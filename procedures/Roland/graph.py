models.py

class XMLGraph(models.Model):
    #only one title per graph
    title = models.OneToOneField(
        to=Title,
        blank=True,
        null=True,
        on_delete=models.CASCADE)

    XMLGraph = models.TextField(null=True)
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.CharField(max_length=20)

    def __str__(self):
        return str(self.XMLGraph)

class Mxcell(models.Model): #Case
	style = models.CharField(max_length=1000)
	value = models.CharField(max_length=1000)
	# objectives = models.ManyToManyField(Objectives)
	objectives = models.ManyToManyField(Objectives)
	
	# XXX Cycle
	# XXX client
	# XXX get

	def __str__(self):
		return self.value

views.py

@csrf_exempt 
def savefile(request):

	member_instance = request.user
	# member_instance = get_object_or_404(Member, user=user)
	print(member_instance)

	
	if request.method == "POST":
		xmlData = request.POST['xml']
		member, _ = Member.objects.get_or_create(user=member_instance)
		# member.user = member_instance;
		# member.save()
		print(member)
# #Get XML data once user presses save
		
		XMLGraph.objects.all().delete()
		xml, _ = XMLGraph.objects.get_or_create(XMLGraph = xmlData)
		print(xml)
		Member.objects.filter(user=member_instance).update(XMLGraph = xml)

		return render_to_response('index.html', content_type="text/xml; encoding=utf-8")
	return HttpResponse('POST is not used')


index.html

<!--[if IE]><meta http-equiv="X-UA-Compatible" content="IE=5,IE=9" ><![endif]-->
<!DOCTYPE html>
{% load static %}
<html>
<head>

    <title>Grapheditor</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
	<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"/>
    <link rel="stylesheet" type="text/css" href="{% static 'styles/grapheditor.css' %}"/>
    <!-- <link rel="stylesheet" type="text/css" href="{% static 'css/common.css' %}"/> -->



	<script type="text/javascript">
		// Parses URL parameters. Supported parameters are:
		// - lang=xy: Specifies the language of the user interface.
		// - touch=1: Enables a touch-style user interface.
		// - storage=local: Enables HTML5 local storage.
		// - chrome=0: Chromeless mode.
		
		var urlParams = (function(url)
		{
			var result = new Object();
			var idx = url.lastIndexOf('?');
	
			if (idx > 0)
			{
				var params = url.substring(idx + 1).split('&amp;');
				
				for (var i = 0; i '&lt;' params.length; i++)
				{
					idx = params[i].indexOf('=');
					
					if (idx '&gt;' 0)
					{
						result[params[i].substring(0, idx)] = params[i].substring(idx + 1);
					}
				}
			}
			
			return result;
		})(window.location.href);
	
		// Default resources are included in grapheditor resources
		mxLoadResources = false;
	</script>



	
	<script type="text/javascript" src="{% static 'js/Init.js' %}"></script>
	<script type="text/javascript" src="{% static 'deflate/pako.min.js' %}"></script>
	<script type="text/javascript" src="{% static 'deflate/base64.js' %}"></script>
	<script type="text/javascript" src="{% static 'jscolor/jscolor.js' %}"></script>
	<script type="text/javascript" src="{% static 'sanitizer/sanitizer.min.js' %}"></script>
	<script type="text/javascript" src="{% static 'js/mxClient.js' %}"></script>
	<script type="text/javascript" src="{% static 'js/EditorUi.js' %}"></script>
	<script type="text/javascript" src="{% static 'js/Editor.js' %}"></script>
	<script type="text/javascript" src="{% static 'js/Sidebar.js' %}"></script>
	<script type="text/javascript" src="{% static 'js/Graph.js' %}"></script>
	<script type="text/javascript" src="{% static 'js/Format.js' %}"></script>
	<script type="text/javascript" src="{% static 'js/Shapes.js' %}"></script>
	<script type="text/javascript" src="{% static 'js/Actions.js' %}"></script>
	<script type="text/javascript" src="{% static 'js/Menus.js' %}"></script>
	<script type="text/javascript" src="{% static 'js/Toolbar.js' %}"></script>
	<script type="text/javascript" src="{% static 'js/Dialogs.js' %}"></script>
	<script src="{% static 'js/jquery-3.3.1.min.js' %}"></script>

	

</head>
 

<body class="geEditor">
	<script type="text/javascript">
		// Extends EditorUi to update I/O action states based on availability of backend
		(function()
		{
			var editorUiInit = EditorUi.prototype.init;

			
			EditorUi.prototype.init = function()
			{
				editorUiInit.apply(this, arguments);
				this.actions.get('export').setEnabled(false);

				// Updates action states which require a backend
				// if (!Editor.useLocalStorage)
				// {
				// 	mxUtils.post(OPEN_URL, '', mxUtils.bind(this, function(req)
				// 	{
				// 		var enabled = req.getStatus() != 404;
				// 		this.actions.get('open').setEnabled(enabled || Graph.fileSupport);
				// 		this.actions.get('import').setEnabled(enabled || Graph.fileSupport);
				// 		this.actions.get('save').setEnabled(enabled);
				// 		this.actions.get('saveAs').setEnabled(enabled);
				// 		this.actions.get('export').setEnabled(enabled);
					
				// 	}));
				// }
			};
			
			// Adds required resources (disables loading of fallback properties, this can only
			// be used if we know that all keys are defined in the language specific file)
			mxResources.loadDefaultBundle = false;
			var bundle = mxResources.getDefaultBundle(src="{% static 'resources/grapheditor' %}", mxLanguage) ||
				mxResources.getSpecialBundle(src="{% static 'resources' %}", mxLanguage);

			// Fixes possible asynchronous requests
			mxUtils.getAll([bundle, src="{% static 'styles' %}" + '/default.xml'], function(xhr)
			{
				// Adds bundle text to resources
				mxResources.parse(xhr[0].getText());
				
				// Configures the default graph theme
				var themes = new Object();
				themes[Graph.prototype.defaultThemeName] = xhr[1].getDocumentElement(); 
				
				
				// Main
				new EditorUi(new Editor(urlParams['chrome'] == '0', themes));

			}, function()
			{
				document.body.innerHTML = '<center style="margin-top:10%;">Error loading resource files. Please check browser console.</center>';

			});
				document.body.appendChild(mxUtils.button('Test', function(evt)
	 		 {
	   alert('Hello, World!');
	 		}));
		})();
	</script>

		<script> 

		var button = mxUtils.button('save', function()
            {

                var encoder = new mxCodec();
                var node = encoder.encode(graph.getModel());
                var xml = mxUtils.getPrettyXml(node); 
                var csrftoken = getCookie('csrftoken');

                $.ajax({

                    type: "POST",
                    url:  "{% url 'savefile' %}" ,
                    data: { "xml": xml},
                    headers:{
                        "X-CSRFToken": csrftoken
                    },
                    success: function(data){
                        console.log("data" + data[0])

                        //functions in mxgraph to decode the xml back to a graph
                        var xmlDoc = mxUtils.parseXml(data[0]);
                        var node = xmlDoc.documentElement;
                        console.log("node " + node)
                        var dec = new mxCodec(node.ownerDocument);
                        //console.log("dec " + dec)
                        //console.log("graph model " + graph.getModel())
                        dec.decode(node, graph.getModel());

                    }
                });

                //console.log(xml);
                // mxUtils.popup(mxUtils.getPrettyXml(node), true);
            });
		document.body.appendChild(button);
		// document.body.insertBefore(button),document.body.firstChild

	
		</script>


</body>
</html>
