import requests
import json
from IPython.core.display import display, HTML

'''
Searches for targets and diseases associated with the drug
'''
def drugSearch(myDrug):

	esURL = 'http://172.17.7.25:80/16.08_evidence-data-generic/_search'

	query = json.dumps({
        	"_source": ["disease.efo_info.label", "drug.molecule_name", "drug.id", "drug.max_phase_for_all_diseases.label", "drug.molecule_type", "target.gene_info.symbol", "evidence.target2drug.mechanism_of_action"],
        	"query": {
            		"match": {
                		"drug.molecule_name": myDrug
            		}
        	}
    	})

	response = requests.get(esURL, data=query)
	#print json.dumps(response.json(), indent=2)
	return organizeResults(response.json())


'''
Organize the results into a data structure that can be used
'''
def organizeResults(output):

	dataObject = {}
	dataObject['diseases'] = set()
	dataObject['targets'] = set()
	dataObject['classification'] = {}
	dataObject['associations'] = {}
	disease = ""
	target = ""

	for data in output['hits']['hits']:
    
		#print json.dumps(data, indent=2)
		
		disease = data['_source']['disease']['efo_info']['label']
		target = data['_source']['target']['gene_info']['symbol']
		dataObject['diseases'].add(disease)
		dataObject['targets'].add(target)
		dataObject['classification']['drug_phase'] = data['_source']['drug']['max_phase_for_all_diseases']['label']
		dataObject['classification']['drug_molecule'] = data['_source']['drug']['molecule_type']
		dataObject['classification']['drug_id'] = data['_source']['drug']['id'][0]

		if target in dataObject['associations']:
			dataObject['associations'][target].add(disease)
		else:
			dataObject['associations'][target] = set()
			dataObject['associations'][target].add(disease)
	
	return dataObject

'''
Display the results in a table
'''
def displayResults(myDrug, dataObject):

	html = """ 
	<head>
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
	</head>
	<body>
		
	""" + "<h1>" + myDrug.upper() + "</h1>" + "<small><a href=" + dataObject['classification']['drug_id'] + ">" + dataObject['classification']['drug_id'] + "</a></small></br>" + """
	<b> """ + dataObject['classification']['drug_phase'] + "&nbsp; &#183; &nbsp;" + dataObject['classification']['drug_molecule'] + "</b>" + """
	
	<hr>
	<div class="row">
		<div class="col-md-6" style="border-right: 1px solid #eee;"><h3>Diseases</h3></br>&#183; """ + "</br> &#183; ".join(dataObject['diseases']) + """</div>
		<div class="col-md-6"><h3>Targets</h3></br>&#183; """ + "</br> &#183; ".join(dataObject['targets']) + """</div>	
	</div>
	<hr>
	</body>

	"""

	return html


def displayFoamTree(myDrug, dataObject):
	
	diseaseArray = []
	targetArray = []
	classificationArray = []
	dataJSON = []
	
	for val in dataObject['diseases']:
		diseaseArray.append({'label': val})

	for val in dataObject['targets']:
		targetArray.append({'label': val})
    
	dataJSON = [{'label': "Diseases", 'weight': 1.0},
           		{'label': "Targets", 'weight': 1.0}
    ]

	dataJSON[0]["groups"] = diseaseArray
	dataJSON[1]["groups"] = targetArray    

	html = """
	<!DOCTYPE html>
	<html>
	  <head>
		<title>FoamTree Quick Start</title>
		<meta charset="utf-8" />
	  </head>

	  <body>
	  
	""" + "<h1>" + myDrug.upper() + "</h1>" + "<small><a href=" + dataObject['classification']['drug_id'] + ">" + dataObject['classification']['drug_id'] + "</a></small></br>" + """
	<b> """ + dataObject['classification']['drug_phase'] + "&nbsp; &#183; &nbsp;" + dataObject['classification']['drug_molecule'] + "</b>" + """
	
	<hr>
		<center><div id="visualization" style="width: 800px; height: 500px"></div></center>

		<script src="carrotsearch.foamtree.js"></script>
		<script>
		  function init() {
			var foamtree = new CarrotSearchFoamTree({
			  id: "visualization",
			  dataObject: {
				groups:""" + json.dumps(dataJSON) + """
			  }
			});
		  }
			
		init();
		</script>
	  </body>
	 """
		
	return html

def displayFlareGraph(myDrug, dataObject):
	
	targetJSON = {}
	dataJSON = {'name': myDrug}
	dataJSON['children'] = []

	for key in dataObject['associations']:
		targetJSON = {'name': key}
		targetJSON['children'] = []
		
		for target in dataObject['associations'][key]:
			
			targetJSON['children'].append({'name': target})

		dataJSON['children'].append(targetJSON)

	html = """
	<!DOCTYPE html>
<meta charset="utf-8">
<title>Flare Dendrogram</title>
<style>

.node circle {
  fill: #fff;
  stroke: steelblue;
  stroke-width: 1.5px;
}

.node {
  font: 10px sans-serif;
}

.link {
  fill: none;
  stroke: #ccc;
  stroke-width: 1.5px;
}

</style>
<body>
"""+ "<h1>" + myDrug.upper() + "</h1>" + "<small><a href=" + dataObject['classification']['drug_id'] + ">" + dataObject['classification']['drug_id'] + "</a></small></br>" + """
	<b> """ + dataObject['classification']['drug_phase'] + "&nbsp; &#183; &nbsp;" + dataObject['classification']['drug_molecule'] + "</b>" + """
	
	<hr>
<div id="flare"></div>
<script src="//d3js.org/d3.v3.min.js"></script>
<script>

var radius = 960 / 2;

var cluster = d3.layout.cluster()
    .size([360, radius - 120]);

var diagonal = d3.svg.diagonal.radial()
    .projection(function(d) { return [d.y, d.x / 180 * Math.PI]; });

var svg = d3.select("#flare").append("svg")
    .attr("width", radius * 2)
    .attr("height", radius * 2)
  .append("g")
    .attr("transform", "translate(" + radius + "," + radius + ")");
    
    var root = """ + json.dumps(dataJSON) + """;

  var nodes = cluster.nodes(root);

  var link = svg.selectAll("path.link")
      .data(cluster.links(nodes))
    .enter().append("path")
      .attr("class", "link")
      .attr("d", diagonal);

  var node = svg.selectAll("g.node")
      .data(nodes)
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })

  node.append("circle")
      .attr("r", 4.5);

  node.append("text")
      .attr("dy", ".31em")
      .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
      .attr("transform", function(d) { return d.x < 180 ? "translate(8)" : "rotate(180)translate(-8)"; })
      .text(function(d) { return d.name; });

d3.select(self.frameElement).style("height", radius * 2 + "px");

</script>
</body>
	
	"""
	return html

def displayNetworkGraph():
	
	html = """
	<!DOCTYPE html>
	<meta charset="utf-8">
	<style>
	body {
	  overflow:hidden;
	   margin:0;
	}

	text {
	  font-family: sans-serif;
	  pointer-events: none;
	}

	</style>
	<body>
	<div id="viz2"></div>
	<script src="http://d3js.org/d3.v3.min.js"></script>
	<script>
	var w = window.innerWidth;
	var h = window.innerHeight;

	var keyc = true, keys = true, keyt = true, keyr = true, keyx = true, keyd = true, keyl = true, keym = true, keyh = true, key1 = true, key2 = true, key3 = true, key0 = true

	var focus_node = null, highlight_node = null;

	var text_center = false;
	var outline = false;

	var min_score = 0;
	var max_score = 1;

	var color = d3.scale.linear()
	  .domain([min_score, (min_score+max_score)/2, max_score])
	  .range(["lime", "yellow", "red"]);

	var highlight_color = "blue";
	var highlight_trans = 0.1;
	  
	var size = d3.scale.pow().exponent(1)
	  .domain([1,100])
	  .range([8,24]);
		
	var force = d3.layout.force()
	  .linkDistance(60)
	  .charge(-300)
	  .size([w,h]);

	var default_node_color = "#ccc";
	//var default_node_color = "rgb(3,190,100)";
	var default_link_color = "#888";
	var nominal_base_node_size = 8;
	var nominal_text_size = 10;
	var max_text_size = 24;
	var nominal_stroke = 1.5;
	var max_stroke = 4.5;
	var max_base_node_size = 36;
	var min_zoom = 0.1;
	var max_zoom = 7;
	var svg = d3.select("#viz2").append("svg");
	var zoom = d3.behavior.zoom().scaleExtent([min_zoom,max_zoom])
	var g = svg.append("g");
	svg.style("cursor","move");

	var graph = {
	  "graph": [],
	  "links": [
		{"source": 0, "target": 1},
		{"source": 0, "target": 2},
		{"source": 1, "target": 3},
		{"source": 2, "target": 4},
		{"source": 2, "target": 5},
		{"source": 2, "target": 6},
		{"source": 2, "target": 7},
		{"source": 2, "target": 8},
		{"source": 2, "target": 9}],
	  "nodes": [
		{"size": 100, "score": 1, "id": "INFLIXIMAB", "type": "square"},
		{"size": 60, "score": 1, "id": "Target", "type": "circle"},
		{"size": 60, "score": 1, "id": "Disease", "type": "circle"},
		{"size": 20, "score": 1, "id": "TNF", "type": "circle"},
		{"size": 20, "score": 1, "id": "acute graft vs. host disease", "type": "circle"},
		{"size": 20, "score": 1, "id": "Crohn's disease", "type": "circle"},
		{"size": 20, "score": 1, "id": "ankylosing spondylitis", "type": "circle"},
		{"size": 20, "score": 1, "id": "rheumatoid arthritis", "type": "circle"},
		{"size": 20, "score": 1, "id": "colitis", "type": "circle"},
		{"size": 20, "score": 1, "id": "spondyloarthropathy", "type": "circle"}
	   ],
	  "directed": false,
	  "multigraph": false
	}


	var linkedByIndex = {};
		graph.links.forEach(function(d) {
		linkedByIndex[d.source + "," + d.target] = true;
		});

		function isConnected(a, b) {
			return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index] || a.index == b.index;
		}

		function hasConnections(a) {
			for (var property in linkedByIndex) {
					s = property.split(",");
					if ((s[0] == a.index || s[1] == a.index) && linkedByIndex[property]) 					return true;
			}
		return false;
		}
		
	  force
		.nodes(graph.nodes)
		.links(graph.links)
		.start();

	  var link = g.selectAll(".link")
		.data(graph.links)
		.enter().append("line")
		.attr("class", "link")
		.style("stroke-width",nominal_stroke)
		.style("stroke", function(d) { 
		if (isNumber(d.score) && d.score>=0) return color(d.score);
		else return default_link_color; })


	  var node = g.selectAll(".node")
		.data(graph.nodes)
		.enter().append("g")
		.attr("class", "node")
		
		.call(force.drag)

		
		node.on("dblclick.zoom", function(d) { d3.event.stopPropagation();
		var dcx = (window.innerWidth/2-d.x*zoom.scale());
		var dcy = (window.innerHeight/2-d.y*zoom.scale());
		zoom.translate([dcx,dcy]);
		 g.attr("transform", "translate("+ dcx + "," + dcy  + ")scale(" + zoom.scale() + ")");
		 
		 
		});
		


		
		var tocolor = "fill";
		var towhite = "stroke";
		if (outline) {
			tocolor = "stroke"
			towhite = "fill"
		}
			
		
		
	  var circle = node.append("path")
	  
	  
		  .attr("d", d3.svg.symbol()
			.size(function(d) { return Math.PI*Math.pow(size(d.size)||nominal_base_node_size,2); })
			.type(function(d) { return d.type; }))
	  
		.style(tocolor, function(d) { 
		if (isNumber(d.score) && d.score>=0) return color(d.score);
		else return default_node_color; })
		//.attr("r", function(d) { return size(d.size)||nominal_base_node_size; })
		.style("stroke-width", nominal_stroke)
		.style(towhite, "white");
		  
					
	  var text = g.selectAll(".text")
		.data(graph.nodes)
		.enter().append("text")
		.attr("dy", ".35em")
		.style("font-size", nominal_text_size + "px")

		if (text_center)
		 text.text(function(d) { return d.id; })
		.style("text-anchor", "middle");
		else 
		text.attr("dx", function(d) {return (size(d.size)||nominal_base_node_size);})
		.text(function(d) { return '\u2002'+d.id; });

		node.on("mouseover", function(d) {
		set_highlight(d);
		})
	  .on("mousedown", function(d) { d3.event.stopPropagation();
		  focus_node = d;
		set_focus(d)
		if (highlight_node === null) set_highlight(d)
		
	}	).on("mouseout", function(d) {
			exit_highlight();

	}	);

			d3.select(window).on("mouseup",  
			function() {
			if (focus_node!==null)
			{
				focus_node = null;
				if (highlight_trans<1)
				{
		
			circle.style("opacity", 1);
		  text.style("opacity", 1);
		  link.style("opacity", 1);
		}
			}
		
		if (highlight_node === null) exit_highlight();
			});

	function exit_highlight()
	{
			highlight_node = null;
		if (focus_node===null)
		{
			svg.style("cursor","move");
			if (highlight_color!="white")
		{
			circle.style(towhite, "white");
		  text.style("font-weight", "normal");
		  link.style("stroke", function(o) {return (isNumber(o.score) && o.score>=0)?color(o.score):default_link_color});
	 }
				
		}
	}

	function set_focus(d)
	{	
	if (highlight_trans<1)  {
		circle.style("opacity", function(o) {
					return isConnected(d, o) ? 1 : highlight_trans;
				});

				text.style("opacity", function(o) {
					return isConnected(d, o) ? 1 : highlight_trans;
				});
				
				link.style("opacity", function(o) {
					return o.source.index == d.index || o.target.index == d.index ? 1 : highlight_trans;
				});		
		}
	}


	function set_highlight(d)
	{
		svg.style("cursor","pointer");
		if (focus_node!==null) d = focus_node;
		highlight_node = d;

		if (highlight_color!="white")
		{
			  circle.style(towhite, function(o) {
					return isConnected(d, o) ? highlight_color : "white";});
				text.style("font-weight", function(o) {
					return isConnected(d, o) ? "bold" : "normal";});
				link.style("stroke", function(o) {
				  return o.source.index == d.index || o.target.index == d.index ? highlight_color : ((isNumber(o.score) && o.score>=0)?color(o.score):default_link_color);

				});
		}
	}
		 
		 
	  zoom.on("zoom", function() {
	  
		var stroke = nominal_stroke;
		if (nominal_stroke*zoom.scale()>max_stroke) stroke = max_stroke/zoom.scale();
		link.style("stroke-width",stroke);
		circle.style("stroke-width",stroke);
		   
		var base_radius = nominal_base_node_size;
		if (nominal_base_node_size*zoom.scale()>max_base_node_size) base_radius = max_base_node_size/zoom.scale();
			circle.attr("d", d3.svg.symbol()
			.size(function(d) { return Math.PI*Math.pow(size(d.size)*base_radius/nominal_base_node_size||base_radius,2); })
			.type(function(d) { return d.type; }))
			
		//circle.attr("r", function(d) { return (size(d.size)*base_radius/nominal_base_node_size||base_radius); })
		if (!text_center) text.attr("dx", function(d) { return (size(d.size)*base_radius/nominal_base_node_size||base_radius); });
		
		var text_size = nominal_text_size;
		if (nominal_text_size*zoom.scale()>max_text_size) text_size = max_text_size/zoom.scale();
		text.style("font-size",text_size + "px");

		g.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
		});
		 
	  svg.call(zoom);	  
		
	  resize();
	  //window.focus();
	  d3.select(window).on("resize", resize).on("keydown", keydown);
		  
	  force.on("tick", function() {
		  
		node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
		text.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
	  
		link.attr("x1", function(d) { return d.source.x; })
		  .attr("y1", function(d) { return d.source.y; })
		  .attr("x2", function(d) { return d.target.x; })
		  .attr("y2", function(d) { return d.target.y; });
			
		node.attr("cx", function(d) { return d.x; })
		  .attr("cy", function(d) { return d.y; });
		});
	  
	  function resize() {
		var width = window.innerWidth, height = window.innerHeight;
		svg.attr("width", width).attr("height", height);
		
		force.size([force.size()[0]+(width-w)/zoom.scale(),force.size()[1]+(height-h)/zoom.scale()]).resume();
		w = width;
		h = height;
		}
		
		function keydown() {
		if (d3.event.keyCode==32) {  force.stop();}
		else if (d3.event.keyCode>=48 && d3.event.keyCode<=90 && !d3.event.ctrlKey && !d3.event.altKey && !d3.event.metaKey)
		{
	  switch (String.fromCharCode(d3.event.keyCode)) {
		case "C": keyc = !keyc; break;
		case "S": keys = !keys; break;
		case "T": keyt = !keyt; break;
		case "R": keyr = !keyr; break;
		case "X": keyx = !keyx; break;
		case "D": keyd = !keyd; break;
		case "L": keyl = !keyl; break;
		case "M": keym = !keym; break;
		case "H": keyh = !keyh; break;
		case "1": key1 = !key1; break;
		case "2": key2 = !key2; break;
		case "3": key3 = !key3; break;
		case "0": key0 = !key0; break;
	  }
		  
	  link.style("display", function(d) {
					var flag  = vis_by_type(d.source.type)&&vis_by_type(d.target.type)&&vis_by_node_score(d.source.score)&&vis_by_node_score(d.target.score)&&vis_by_link_score(d.score);
					linkedByIndex[d.source.index + "," + d.target.index] = flag;
				  return flag?"inline":"none";});
	  node.style("display", function(d) {
					return (key0||hasConnections(d))&&vis_by_type(d.type)&&vis_by_node_score(d.score)?"inline":"none";});
	  text.style("display", function(d) {
					return (key0||hasConnections(d))&&vis_by_type(d.type)&&vis_by_node_score(d.score)?"inline":"none";});
					
					if (highlight_node !== null)
					{
						if ((key0||hasConnections(highlight_node))&&vis_by_type(highlight_node.type)&&vis_by_node_score(highlight_node.score)) { 
						if (focus_node!==null) set_focus(focus_node);
						set_highlight(highlight_node);
						}
						else {exit_highlight();}
					}

	}	
	}
	 


	function vis_by_type(type)
	{
		switch (type) {
		  case "circle": return keyc;
		  case "square": return keys;
		  case "triangle-up": return keyt;
		  case "diamond": return keyr;
		  case "cross": return keyx;
		  case "triangle-down": return keyd;
		  default: return true;
	}
	}
	function vis_by_node_score(score)
	{
		if (isNumber(score))
		{
		if (score>=0.666) return keyh;
		else if (score>=0.333) return keym;
		else if (score>=0) return keyl;
		}
		return true;
	}

	function vis_by_link_score(score)
	{
		if (isNumber(score))
		{
		if (score>=0.666) return key3;
		else if (score>=0.333) return key2;
		else if (score>=0) return key1;
	}
		return true;
	}

	function isNumber(n) {
	  return !isNaN(parseFloat(n)) && isFinite(n);
	}


	</script>
	</body>

	"""

	return html

def displayBubbleMenu(myDrug, dataObject):
	
	diseaseArray = []
	targetArray = []
	classificationArray = []
	dataJSON = []
	
	for val in dataObject['diseases']:
		diseaseArray.append({'name': val})

	for val in dataObject['targets']:
		targetArray.append({'name': val})
		
	dataJSON = {'name': 'bubble', 'children': [{'name': "Diseases"},
           		{'name': "Targets"}
    ]}

	dataJSON['children'][0]["children"] = diseaseArray
	dataJSON['children'][1]["children"] = targetArray    

	html = """
<style type="text/css">
    #mainBubble {
      background: #fff;
      border: solid 1px #ddd;
      box-shadow: 0 0 4px rgba(0,0,0,0);
      font: 10px sans-serif;
      height: 800px;
      position: relative;
      width: 80%;
    }
             
    #mainBubble svg {
      left: 0;
      position: absolute;
      top: 0;
    }
                         
    #mainBubble circle.topBubble {
      fill: #aaa;
      stroke: #666;
      stroke-width: 1.5px;
     }
    </style>
    <script type="text/javascript" src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
  """+ "<h1>" + myDrug.upper() + "</h1>" + "<small><a href=" + dataObject['classification']['drug_id'] + ">" + dataObject['classification']['drug_id'] + "</a></small></br>" + """
	<b> """ + dataObject['classification']['drug_phase'] + "&nbsp; &#183; &nbsp;" + dataObject['classification']['drug_molecule'] + "</b>" + """
	
	<hr> 
  <div id="mainBubble" style="height: 652px; width:950px"><svg class="mainBubbleSVG" width="930.24" height="652"></svg></div>
  <script>
  // http://sunsp.net/demo/BubbleMenu/
  
   var w = window.innerWidth;
   var h = Math.ceil(w*0.7);
   var oR = 0;
   var nTop = 0;
    
   var svgContainer = d3.select("#mainBubble")
      .style("height", h+"px");
    
   var svg = d3.select("#mainBubble").append("svg")
        .attr("class", "mainBubbleSVG")
        .attr("width", w)
        .attr("height",h)
        .on("mouseleave", function() {return resetBubbles();});
         
   var mainNote = svg.append("text")
    .attr("id", "bubbleItemNote")
    .attr("x", 10)
    .attr("y", w/2-15)
    .attr("font-size", 12)
    .attr("dominant-baseline", "middle")
    .attr("alignment-baseline", "middle")
    .style("fill", "#888888")
    
    var root = """ + json.dumps(dataJSON) + """;
     
        var bubbleObj = svg.selectAll(".topBubble")
                .data(root.children)
            .enter().append("g")
                .attr("id", function(d,i) {return "topBubbleAndText_" + i});
             
        console.log(root);  
        nTop = root.children.length;
        oR = w/(1+3*nTop);  
 
    h = Math.ceil(w/nTop*2);
    svgContainer.style("height",h+"px");
         
        var colVals = d3.scale.category10();
         
        bubbleObj.append("circle")
            .attr("class", "topBubble")
            .attr("id", function(d,i) {return "topBubble" + i;})
            .attr("r", function(d) { return oR; })
            .attr("cx", function(d, i) {return oR*(3*(1+i)-1);})
            .attr("cy", (h+oR)/3)
            .style("fill", function(d,i) { return colVals(i); }) // #1f77b4
        .style("opacity",0.3)
            .on("mouseover", function(d,i) {return activateBubble(d,i);});
         
             
        bubbleObj.append("text")
            .attr("class", "topBubbleText")
            .attr("x", function(d, i) {return oR*(3*(1+i)-1);})
            .attr("y", (h+oR)/3)
        .style("fill", function(d,i) { return colVals(i); }) // #1f77b4
            .attr("font-size", 30)
            .attr("text-anchor", "middle")
        .attr("dominant-baseline", "middle")
        .attr("alignment-baseline", "middle")
            .text(function(d) {return d.name})      
            .on("mouseover", function(d,i) {return activateBubble(d,i);});
         
         
        for(var iB = 0; iB < nTop; iB++)
        {
            var childBubbles = svg.selectAll(".childBubble" + iB)
                .data(root.children[iB].children)
                .enter().append("g");
                 
        //var nSubBubble = Math.floor(root.children[iB].children.length/2.0);   
             
            childBubbles.append("circle")
                .attr("class", "childBubble" + iB)
                .attr("id", function(d,i) {return "childBubble_" + iB + "sub_" + i;})
                .attr("r",  function(d) {return oR/3.0;})
                .attr("cx", function(d,i) {return (oR*(3*(iB+1)-1) + oR*1.5*Math.cos((i-1)*45/180*3.1415926));})
                .attr("cy", function(d,i) {return ((h+oR)/3 +        oR*1.5*Math.sin((i-1)*45/180*3.1415926));})
                .attr("cursor","pointer")
                .style("opacity",0.5)
                .style("fill", "#eee")
                .on("click", function(d,i) {
                window.open(d.address);                 
              })
            .on("mouseover", function(d,i) {
              //window.alert("say something");
              var noteText = "";
              if (d.note == null || d.note == "") {
                noteText = d.address;
              } else {
                noteText = d.note;
              }
              })
            .append("svg:title")
            .text(function(d) { return d.address; });   
 
            childBubbles.append("text")
                .attr("class", "childBubbleText" + iB)
                .attr("x", function(d,i) {return (oR*(3*(iB+1)-1) + oR*1.5*Math.cos((i-1)*45/180*3.1415926));})
                .attr("y", function(d,i) {return ((h+oR)/3 +        oR*1.5*Math.sin((i-1)*45/180*3.1415926));})
                .style("opacity",0.5)
                .attr("text-anchor", "middle")
            .style("fill", function(d,i) { return colVals(iB); }) // #1f77b4
                .attr("font-size", 6)
                .attr("cursor","pointer")
                .attr("dominant-baseline", "middle")
            .attr("alignment-baseline", "middle")
                .text(function(d) {return d.name})      
                .on("click", function(d,i) {
                window.open(d.address);
                }); 
 
        }
 
         
 
    resetBubbles = function () {
      w = window.innerWidth*0.68*0.95;
      oR = w/(1+3*nTop);
       
      h = Math.ceil(w/nTop*2);
      svgContainer.style("height",h+"px");
 
      mainNote.attr("y",h-15);
           
      svg.attr("width", w);
      svg.attr("height",h);       
       
      
      var t = svg.transition()
          .duration(650);
         
        t.selectAll(".topBubble")
            .attr("r", function(d) { return oR; })
            .attr("cx", function(d, i) {return oR*(3*(1+i)-1);})
            .attr("cy", (h+oR)/3);
 
        t.selectAll(".topBubbleText")
        .attr("font-size", 30)
            .attr("x", function(d, i) {return oR*(3*(1+i)-1);})
            .attr("y", (h+oR)/3);
     
      for(var k = 0; k < nTop; k++) 
      {
        t.selectAll(".childBubbleText" + k)
                .attr("x", function(d,i) {return (oR*(3*(k+1)-1) + oR*1.5*Math.cos((i-1)*45/180*3.1415926));})
                .attr("y", function(d,i) {return ((h+oR)/3 +        oR*1.5*Math.sin((i-1)*45/180*3.1415926));})
            .attr("font-size", 6)
                .style("opacity",0.5);
 
        t.selectAll(".childBubble" + k)
                .attr("r",  function(d) {return oR/3.0;})
            .style("opacity",0.5)
                .attr("cx", function(d,i) {return (oR*(3*(k+1)-1) + oR*1.5*Math.cos((i-1)*45/180*3.1415926));})
                .attr("cy", function(d,i) {return ((h+oR)/3 +        oR*1.5*Math.sin((i-1)*45/180*3.1415926));});
                     
      }   
    }
         
         
        function activateBubble(d,i) {
            // increase this bubble and decrease others
            var t = svg.transition()
                .duration(d3.event.altKey ? 7500 : 350);
     
            t.selectAll(".topBubble")
                .attr("cx", function(d,ii){
                    if(i == ii) {
                        // Nothing to change
                        return oR*(3*(1+ii)-1) - 0.6*oR*(ii-1);
                    } else {
                        // Push away a little bit
                        if(ii < i){
                            // left side
                            return oR*0.6*(3*(1+ii)-1);
                        } else {
                            // right side
                            return oR*(nTop*3+1) - oR*0.6*(3*(nTop-ii)-1);
                        }
                    }               
                })
                .attr("r", function(d, ii) { 
                    if(i == ii)
                        return oR*1.8;
                    else
                        return oR*0.8;
                    });
                     
            t.selectAll(".topBubbleText")
                .attr("x", function(d,ii){
                    if(i == ii) {
                        // Nothing to change
                        return oR*(3*(1+ii)-1) - 0.6*oR*(ii-1);
                    } else {
                        // Push away a little bit
                        if(ii < i){
                            // left side
                            return oR*0.6*(3*(1+ii)-1);
                        } else {
                            // right side
                            return oR*(nTop*3+1) - oR*0.6*(3*(nTop-ii)-1);
                        }
                    }               
                })          
                .attr("font-size", function(d,ii){
                    if(i == ii)
                        return 30*1.5;
                    else
                        return 30*0.6;              
                });
     
            var signSide = -1;
            for(var k = 0; k < nTop; k++) 
            {
                signSide = 1;
                if(k < nTop/2) signSide = 1;
                t.selectAll(".childBubbleText" + k)
                    .attr("x", function(d,i) {return (oR*(3*(k+1)-1) - 0.6*oR*(k-1) + signSide*oR*2.5*Math.cos((i-1)*45/180*3.1415926));})
                    .attr("y", function(d,i) {return ((h+oR)/3 + signSide*oR*2.5*Math.sin((i-1)*45/180*3.1415926));})
                    .attr("font-size", function(){
                            return (k==i)?12:6;
                        })
                    .style("opacity",function(){
                            return (k==i)?1:0;
                        });
                     
                t.selectAll(".childBubble" + k)
                    .attr("cx", function(d,i) {return (oR*(3*(k+1)-1) - 0.6*oR*(k-1) + signSide*oR*2.5*Math.cos((i-1)*45/180*3.1415926));})
                    .attr("cy", function(d,i) {return ((h+oR)/3 + signSide*oR*2.5*Math.sin((i-1)*45/180*3.1415926));})
                    .attr("r", function(){
                            return (k==i)?(oR*0.55):(oR/3.0);               
                    })
                    .style("opacity", function(){
                            return (k==i)?1:0;                  
                        }); 
            }                   
        }
     
    window.onresize = resetBubbles;
	</script>
	"""
	
	return html