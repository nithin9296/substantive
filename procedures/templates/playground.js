
var mxClient = {

  VERSION: '3.9.12',

  IS_SVG: navigator.userAgent.indexOf('AppleWebKit/') >= 0,

  isBrowserSupported: function () {
    return mxClient.IS_VML || mxClient.IS_SVG
  },

  // Because it is a function inside some object, Link is used to declare the function name
  link: function (rel, href, doc) {
    doc = doc || document

    if (mxClient.IS_IE6) {
      doc.write('<link rel="' + rel + '" href="' + href + '" charset="UTF-8" type="text/css/>')
    } else {
      var link = doc.createlement('link')

      link.setAttribute('rel', rel)// set attribute adds specified attribute to an element and gives it a specific value
      link.setAttribute('href', href)
      link.setAttribute('charset', 'UTF-8')
      link.setAttribute('type', 'test/css')

      var head = doc.getElementsByTagName('head')[0]
      head.appendChild(link)
    }
  },

  loadResources: function (fn, lan) {
  	var pending = mxClient.defaultBundles.length

  	function callback () {
  		if (--pending == 0) { // If equal to --is decrement by2
  			fn()
  		}
  	}
  	for (var i = 0; i < mxClient.defaultBundles.length; i++) {
  		mxResoruces.add(mxClient.defaultBundles[i], lan, callback)
  	}
  },

  // Include FUnction - Dynamically adds a script node to the document header
  include: function (src) {
  	document.write('<script src="' + src + '"></script>')
  }
}

// Varaiable: mxLoadResources  - Optional global config variable to toggle loading of the two resource files in <mxgraph> and <mxeditor>
if (typeof (mxLoadResources) === 'undefined') {
  	mxLoadResources = true
}

// Varaible: mxForceIncludes - Optional global config variable to force loading of javascript files in development mode

if (typeof (mxForceIncludes) === 'undefined') {
  	mxForceIncludes = false
}

// variable mxResoruceExtension - Optional global config variable to specify the extension of the resource files

if (typeof (mxResourceExtension) === 'undefined') {
  	mxResourceExtension = '.txt'
}

// Variable mxLoadStylesheets - Optional global variable to toggle loading of css files when the liabrary is initilised
if (typeof (mxLoadStylesheet) === 'undefined') {
  	mxLoadStylesheet = true
}
// Variable basepath - Basepath for all urls in the core without trailing slash. Default is '.'
/**
   * (code)
 * <script type="text/javascript">
 * 		mxBasePath = '/path/to/core/directory';
 * </script>
 * <script type="text/javascript" src="/path/to/core/directory/js/mxClient.js"></script>
 * (end)
*/

if (typeof (mxBasePath) !== 'undefined' && mxBasePath.length > 0) {
  // Adds trailing slash if required
  if (mxBasePath.substring(mxBasePath.length - 1) == '/') { // Substring method extracts the characters from the string and returns new  substring
    mxBasePath = mxBasePath.substring(0, mxBasePath.length - 1)
  }
  mxClient.basepath = mxBasePath
} else {
  mxClient.basepath = '.'
}

/** Variable ImageBasePath
Base path for all the images urls in the core without trailing slash.
*/
if (typeof (mxImageBasePath) !== 'undefined' && mxImageBasePath.length > 0) {
  if (mxImageBasePath.substring(mxImageBasePath.length - 1) == '/') {
    mxImageBasePath = mxImageBasePath.substring(0, mxImageBasePath.length - 1)
  }
  mxClient.imageBasePath = mxImageBasePath
} else {
  mxClient.imageBasePath = mxClient.basepath + '/images'
}

/** Variable - Language - Defines the language for the client for Eg - en for english
*/

if (typeof (mxLanguage) !== 'undefined' && mxLanguage != null) {
  mxClient.language = mxLanguage
} else {
  mxClient.language = (mxClient.IS_IE) ? navigator.userlangugage : navigator.language
}

if (typeof (mxDefaultLanguage) !== 'undefined' && mxDefaultLanguage != null) {
  mxClient.defaultLanguage = mxDefaultLanguage
} else {
  mxClient.defaultLanguage = 'en'
}

// Adds required namespaces, stylesheets and memory handlers for older IE browsers

if (mxClient.IS_VML) {
  if (mxClient.IS_SVG) {
    mxClient.IS_VML = false
  } else {
    // Enables support for IE8 standards mode. Note that this requires all attributes for VML
    // elements to be set using direct notation, ie. node.attr = value. The use of setAttribute
    // is not possible.
    if (document.documentMode == 8) {
      document.namespaces.add(mxClient.VML_PREFIX, 'urn:schemas-microsoft-com:vml', '#default#VML')
      document.namespaces.add(mxClient.OFFICE_PREFIX, 'urn:schemas-microsoft-com:office:office', '#default#VML')
    } else {
      document.namespaces.add(mxClient.VML_PREFIX, 'urn:schemas-microsoft-com:vml')
      document.namespaces.add(mxClient.OFFICE_PREFIX, 'urn:schemas-microsoft-com:office:office')
    }

    // Workaround for limited number of stylesheets in IE (does not work in standards mode)
    if (mxClient.IS_QUIRKS && document.styleSheets.length >= 30) {
      (function () {
        var node = document.createElement('style')
        node.type = 'text/css'
        node.styleSheet.cssText = mxClient.VML_PREFIX + '\\:*{behavior:url(#default#VML)}' +
		        	mxClient.OFFICE_PREFIX + '\\:*{behavior:url(#default#VML)}'
		        document.getElementsByTagName('head')[0].appendChild(node)
      })()
    } else {
      document.createStyleSheet().cssText = mxClient.VML_PREFIX + '\\:*{behavior:url(#default#VML)}' +
		    	mxClient.OFFICE_PREFIX + '\\:*{behavior:url(#default#VML)}'
    }

	    if (mxLoadStylesheets) {
	    	mxClient.link('stylesheet', mxClient.basePath + '/css/explorer.css')
	    }
  }
}

var mxLog =

{

  // Class: mxLog, A singleton class that implements a simple console.
  // Variable - consolename - specifies the name of the console window

  consoleName: 'Console',
  // Variable - Trace - specifies whether the output for <enter> or <leave> should be visible in the console
  TRACE: false,
  // Variable - Debug - specifies if the output for debug is visible in the console
  DEBUG: true,
  // Variabe -   WARN - Specifies if the output for warn should be visible in the console, default is true
  WARN: true,
  // buffer - buffer for preinitialized content
  buffer: '',

  // Init - Function Init initializes the DOM node for the console.
  // This requires document.body to point to a non-null value. This is called from within <setVisible> if the log is not yet initialised
  // NODE - TO add new element to the HTML DOM, you must create the element (element node) first and then append to the existing element

  init: function () {
  	if (mxlog.window == null && document.body != null) {
  		var title = mxLog.consoleName + ' - mxGraph ' + mxClient.VERSION

  		// Create a table that maintains the layout
  		var table = document.createElement('table')
  		table.setAttribute('width', '100%')
  		table.setAttribute('height', '100%')

  		var tbody = document.createElement('tbody')
  		var tr = document.createElement('tr')
  		var td = document.createElement('td')
  		td.style.verticalAlign = 'top'

  		// Adds the actual console as the text area

  		mxLog.textarea = document.createElement('textarea')
  		mxLog.textarea.setAttribute('wrap', 'off')
      	mxLog.textarea.setAttribute('readOnly', 'true')
      	mxLog.textarea.style.height = '100%'
      	mxLog.textarea.style.resize = 'none'
      	mxLog.textarea.value = mxLog.buffer

      	td.appendChild(mxLog.textarea)
      	tr.appendChild(td)
      	tbody.appendChild(tr)

      	// Creates the container div
      	tr = document.createElement('tr')
      	mxLog.td = document.createElement('td')
      	mxLog.td.style.verticalAlign = 'top'
      	mxLog.td.setAttribute('height', '30px')

      	tr.appendChild(mxLog.td)
      	tbody.appendChild(tr)
      	table.appendChild(tbody)

      	mxLog.addButton('Info', function (evt) {
      		mxLog.info()
      	})

      	mxLog.addButton('DOM', function (evt) {
      		var content = mxUtils.getInnerHtml(document.body)
      		mxLog.debug(content)
      	})

      	mxLog.addButton('Trace', function (evt) {
      		mxLog.TRACE = !mxLog.TRACE

      		if (mxLog.TRACE) {
      			mxLog.debug('Tracing enabled')
      		} else {
      			mxLog.debug('Tracing disabled')
      		}
      	})
      	mxLog.addButton('Copy', function (evt) {
        	try {
          	mxUtils.copy(mxLog.textarea.value)
        	} catch (err) {
         	 mxUtils.alert(err)
        	}
      	})

      	mxLog.addButton('Show', function (evt) {
        	try {
          	mxUtils.popup(mxLog.textarea.value)
        	} catch (err) {
         	 mxUtils.alert(err)
        	}
      	})

      	mxLog.addButton('Clear', function (evt) {
       	 mxLog.textarea.value = ''
      	})

      	// Cross Border code to get window size
      	var h = 0
      	var w = 0

      	if (typeof (window.innerWidth) === 'number') {
      		h = window.innerHeight
      		w = window.innerWidth
      	} else {
      		h = (document.documentElement.clientHeight || document.body.clientHeight)
      		w = document.body.clientWidth
      	}
      	mxLog.window = new mxWindow(title, table, Math.max(0, w - 320), Math.max(0, h - 210), 300, 160)
      mxLog.window.setMaximizable(true)
      mxLog.window.setScrollable(false)
      mxLog.window.setResizable(true)
      mxLog.window.setClosable(true)
      mxLog.window.destroyOnClose = false

      // Workaround for ignored textarea height in various setups
      if (((mxClient.IS_NS || mxClient.IS_IE) && !mxClient.IS_GC &&
				!mxClient.IS_SF && document.compatMode != 'BackCompat') ||
				document.documentMode == 11) {
        var elt = mxLog.window.getElement()

        var resizeHandler = function (sender, evt) {
          mxLog.textarea.style.height = Math.max(0, elt.offsetHeight - 70) + 'px'
        }

        mxLog.window.addListener(mxEvent.RESIZE_END, resizeHandler)
        mxLog.window.addListener(mxEvent.MAXIMIZE, resizeHandler)
        mxLog.window.addListener(mxEvent.NORMALIZE, resizeHandler)

        mxLog.textarea.style.height = '92px'
      }
    }
  },

  	// Function - Info
  	// Writes the current navigator information to the console

  	info: function () {
  		mxLog.writeln(mxUtils.toString(navigator))
  	},

  	// Function - addButton - Adds a button to the console using the given label and function

  	addButton: function (lab, funct) {
  		var button = document.createElement('button')
  		mxUtils.write(button, lab)
  		mxEvent.addListener(button, 'click', funct)
  		mxLog.td.appendChild(button)
  	},

  	// Function - isVisible - Returns true if the console is visible
  	isVisible: function () {
  		if (mxLog.window != null) {
  			return mxLog.window.isVisible()
  		}
  		return false
  	},

  	show: function () {
  		mxLog.setVisible(true)
  	},

  	// Setvisible - shows or hides the console

  	setVisible: function (visible) {
  		if (mxLog.window == null) {
  			mxLog.init()
  		}
  	},
  	enter: function (string) {
    if (mxLog.TRACE) {
      mxLog.writeln('Entering ' + string)

      return new Date().getTime()
    }
  },

  	 leave: function (string, t0) {
    if (mxLog.TRACE) {
      var dt = (t0 != 0) ? ' (' + (new Date().getTime() - t0) + ' ms)' : ''
      mxLog.writeln('Leaving ' + string + dt)
    }
  },

  debug: function () {
    if (mxLog.DEBUG) {
      mxLog.writeln.apply(this, arguments)
    }
  },

  warn: function () {
    if (mxLog.WARN) {
      mxLog.writeln.apply(this, arguments)
    }
  },

  // Write - Adds specific string to the console
  write: function () {
  	var string = ''

  	for (var i = 0; i < arguments.length; i++) {
  		string += arguments[i]

  		if (i <	arguments.length - 1) {
  			string += ' '
  		}
  	}

    if (mxLog.textarea != null) {
      mxLog.textarea.value = mxLog.textarea.value + string

      // Workaround for no update in Presto 2.5.22 (Opera 10.5)
      if (navigator.userAgent.indexOf('Presto/2.5') >= 0) {
        mxLog.textarea.style.visibility = 'hidden'
        mxLog.textarea.style.visibility = 'visible'
      }

      mxLog.textarea.scrollTop = mxLog.textarea.scrollHeight
    } else {
      mxLog.buffer += string
    }
  }

}

var mxObjectIdentity =
{

/** Class: mxObjectIdentity
Identity for Javascript objects and functions. This is implemented using simple incrementing counter  which is stored in each <object> under field name

*/

  FIELD_NAME: 'mxObjectId',

  counter: 0,

  // Function -Get- Return ID for the given object or function or null if no object

  get: function (obj) {
    if (obj != null) {
      if (obj[mxObjectIdentity.FIELD_NAME] == null) {
        if (typeof obj === 'object') {
          var ctor = mxUtils.getFunctionName(obj.constructor)
          obj[mxObjectIdentity.FIELD_NAME] = ctor + '#' + mxObjectIdentity.counter++
        } else if (typeof obj === 'function') {
          obj[mxObjectIdentity.FIELD_NAME] = 'Function#' + mxObjectIdentity.counter++
        }
      }
      return obj[mxObjectIdentity.FIELD_NAME]
    }
    return null
  },

  clear: function (obj) {
    if (typeof (obj) === 'object' || typeof obj === 'function') {
      delete obj[mxObjectIdentity.FIELD_NAME]
    }
  }

}

/** Class - mxDictionary
A wrapper class for an associated array with object keys.

Note - This implementation uses <mxObjectIdentity> to turn object keys into strings

Contructor - mxEventSource
Contructs a new dictioary which allows object to be used as keys

*/

function mxDictionary () {
  this.clear()
};

/** Function - MAP - stores the (key, value) pairs in this dictionary
*/

// All javascript objects inherit properties and methods from prototype

mxDictionary.prototype.map = null

// Function - Clear - Clears the dictionary

mxDictionary.prototype.clear = function () {
  this.map = {}
}

// Function - get - returns the value for the given key.

mxDictionary.prototype.get = function (key) {
  var id = mxObjectIdentity.get(key)

  return this.map[id]
}

// Function - Put - Stores the value under the given key and returns the previous value for that key

mxDictionary.prototype.put = function (key, value) {
  var id = mxObjectIdentity.get(key)
  var previous = this.map[id]
  this.map[id] = value

  return previous
}

/**
 * Function: remove
 *
 * `Removes the value for the given key and returns the value that
 * has been removed.
 */
mxDictionary.prototype.remove = function (key) {
  var id = mxObjectIdentity.get(key)
  var previous = this.map[id]
  delete this.map[id]

  return previous
}

/**
 * Function: getKeys
 *
 * Returns all keys as an array.
 */
mxDictionary.prototype.getKeys = function () {
  var result = []

  for (var key in this.map) {
    result.push(key)
  }

  return result
}

/**
 * Function: getValues
 *
 * Returns all values as an array.
 */
mxDictionary.prototype.getValues = function () {
  var result = []

  for (var key in this.map) {
    result.push(this.map[key])
  }

  return result
}

/**
 * Function: visit
 *
 * Visits all entries in the dictionary using the given function with the
 * following signature: function(key, value) where key is a string and
 * value is an object.
 *
 * Parameters:
 *
 * visitor - A function that takes the key and value as arguments.
 */
mxDictionary.prototype.visit = function (visitor) {
  for (var key in this.map) {
    visitor(key, this.map[key])
  }
}


var mxResources = 
{

	/** Class - mxResources - implements internationalization, You can provide any number of resource files on the server usinmg the following format for the filename.

	*/

	resources: {},

	// Variable - extension, specifies the extension used for langugage files

	extension: mxResourceExtension,

	//Varaible: Resource encoded, specifies whether or not values in the resource files are encoded with /u or percentage

	resourcesEncoded: false,

	//Loaddeafultbundle: specifies if the default file for a given base name should be loaded

	Loaddeafultbundle: true,

	//Function - is langugage supported - Hook for subclassers to disable support for a given langugage.

	isLangugageSupported: function(lan) {
		if (mxClient.langugages != null) {
			return mxUtils.indexOf(mxClient.langugages, lan) >= 0
		}
		return true
	},

	/** Function - getDefaultBundle - Hook for subclassers to return the url for the special bundle. This implementation returns basename + <extension> or null
	if <loadDefaultBundle> is false
		*/

	getDefaultBundle: function (basename, lan) {
		if (mxResources.loadDefaultBundle || !mxResources.isLangugageSupported(lan)) {
			return basename + mxResources.extension
		} else {
			return null
		}
	},

	//Function - getspecialbundle - Hook for subcalssers to return the URL for the special bundle. 

	getSpecialBundle: function (basename, lan) {
		if (mxClient.langugages == null || !this.isLangugageSupported(lan)) {
			var dash = lan.indexOf('-')

			if (dash > 0) {
				lan = lan.substring(0, dash)
			}
		}
		f (mxResources.loadSpecialBundle && mxResources.isLanguageSupported(lan) && lan != mxClient.defaultLanguage) {
      return basename + '_' + lan + mxResources.extension
    } else {
      return null
    }
	},

	/** add - Adds the default and current language properties file for the specified basename. */

	add: function (basename, lan, callback) {
		lan = (lan != null) ? lan : ((mxClient.language != null)
			? mxClient.langugage.toLowerCase() : mxConstants.NONE)

		if (lan != mxConstants.NONE) {
			var defaultBundle = mxResources.getDefaultBundle(basename, lan)
			var specialBundle = mxResources.getspecialbundle(basename, lan)

			var loadSpecialBundle = function () {
				if (specialBundle != null) {
					if (callback) {
						mxUtils.get(specialBundle, function(req) {
							mxResources.parse(req.getText())
              callback()
            }, function () {
              callback()
            })
          } else {
            try {
					   		var req = mxUtils.load(specialBundle)

					   		if (req.isReady()) {
					 	   		mxResources.parse(req.getText())
					   		}
				   		} catch (e) {
				   			// ignore
					   	}
          }
        } else if (callback != null) {
          callback()
        }
      }

      if (defaultBundle != null) {
        if (callback) {
          mxUtils.get(defaultBundle, function (req) {
            mxResources.parse(req.getText())
            loadSpecialBundle()
          }, function () {
            loadSpecialBundle()
          })
        } else {
          try {
				   		var req = mxUtils.load(defaultBundle)

				   		if (req.isReady()) {
				 	   		mxResources.parse(req.getText())
				   		}

				   		loadSpecialBundle()
				  	} catch (e) {
				  		// ignore
				  	}
        }
      } else {
        // Overlays the language specific file (_lan-extension)
        loadSpecialBundle()
      }
    }
  },


  //Function - Get- returns the value for the specified resource key- 

  get: function (key, params, defaultValue) {
  	var value = mxResources.resources[key]

  	if (value == null) {
  		value = defaultValue
  	}

  	if (value != null && params != null) {
  		value = mxResources.replacePlaceholders(value, params)
  	}
  	return value
  },
}


  /** Class - mxPoint, Implements a 2 dimensional vector with a double precision cordinates. 
  constructor - mxPoint, constructs a new point for the optional x and y cordinates 
  */

  function mxPoint (x, y) {
  	this.x = (x != null) ? x : 0 //? assigns a value on condition that X is not equal to null
  	this.y = (y != null) ? y : 0
  };

  //Variable x - holds the x-cordinate of the point. Default is 0

  mxPoint.prototype.x = null
  mxPoint.prototype.y = null

  //Returns true if the given object equals this point

  mxPoint.prototype.equals = function (obj) {
  	returns obj != null && obj.x == this.x && obj.y == this.y
  }

//Function - Clone - Returns clone of this <mxpoint>
mxPoint.prototype.clone = function () {
	return mxUtils.clone(this)
}

/** mxRectangle - Extends <mxPoint> to implement a 2 dimensional rectangle with double precision coordinates

Constructor - Rectangle - contructs a new rectangle for the optional parameters. if no parameteres are given then the respecitve default value is used.
*/

function mxRectangle (x, y, width, height) {
	mxPoint.call(this, x, y) //Call method is can be used to invoke/call a method with an owner object as parameter

	this.width = (width != null) ? width : 0
	this.height = (width != null) ? height : 0
};

mxRectangle.prototype = new mxPoint()
mxRectangle.prototype.constructor = mxRectangle

// Varaible Width - holds the width of the rectangle - default = 0
mxRectangle.prototype.width = null

//Variable height - holds the height of the rectangle - default = 0
mxRectangle.prototype.height = null

//Function - setRect - sets this rectangle to specific value

mxRectangle.prototype.setRect = functiion (x, y, w, h) {
	this.x = x
	this.y = y
	this.width = width
	this.height = height
}

//Function - getCenterX - returns X cordinate of the center point

mxRectangle.prototype.getCenterX = function () {
	return this.x + this.width / 2
}

mxRectangle.prototype.getCentery = function () {
	return this.y + this.height / 2
}

// Function- ADD - Adds the given rectangle to this rectangle

mxRectangle.prototype.add = function (rect) {
	if (rect != null) {
		var minX = Math.min(this.x, rect.x)
		var minY = Math.min(this.y, rect.y)
		var maxX = Math.max(this.x + this.width, rect.x + rect.width)
		var maxY = Math.max(this.y + this.height, rect.y + rect.height)

		this.x = mixX
		this.Y = minY
		this.width = maxX - minX
		this.height = maxY - minY

	}
}

//Function - Intersect - changes rectangle to where it overlaps to the given rectangle

mxRectangle.prototype.intersect = function (rect) {
  if (rect != null) {
    var r1 = this.x + this.width
    var r2 = rect.x + rect.width

    var b1 = this.y + this.height
    var b2 = rect.y + rect.height

    this.x = Math.max(this.x, rect.x)
    this.y = Math.max(this.y, rect.y)
    this.width = Math.min(r1, r2) - this.x
    this.height = Math.min(b1, b2) - this.y
  }
}

mxRectangle.prototype.grow = function (amount) {
  this.x -= amount
  this.y -= amount
  this.width += 2 * amount
  this.height += 2 * amount
}

mxRectangle.prototype.getPoint = function () {
  return new mxPoint(this.x, this.y)
}

mxRectangle.prototype.rotate90 = function () {
  var t = (this.width - this.height) / 2
  this.x += t
  this.y -= t
  var tmp = this.width
  this.width = this.height
  this.height = tmp
}


var mxEffects = {



	/** Class - mxeffects - Provides animation effect, 

	Parameteres - graph - MXgraph that recevies the changes
				changes - an array of changes to be animated
				*/

	animateChanges: function (graph, changes, done) {
		var maxStep = 10
		var step = 0

		var animate = function () {
			var isRequired = false

			for (var i = 0; i < changes.length; i++) {
				var change = changes[i]

			        if (change instanceof mxGeometryChange ||
					change instanceof mxTerminalChange ||
					change instanceof mxValueChange ||
					change instanceof mxChildChange ||
					change instanceof mxStyleChange) {
          var state = graph.getView().getState(change.cell || change.child, false)

          if (state != null) {
            isRequired = true

            if (change.constructor != mxGeometryChange || graph.model.isEdge(change.cell)) {
              mxUtils.setOpacity(state.shape.node, 100 * step / maxStep)
            } else {
              var scale = graph.getView().scale

              var dx = (change.geometry.x - change.previous.x) * scale
              var dy = (change.geometry.y - change.previous.y) * scale

              var sx = (change.geometry.width - change.previous.width) * scale
              var sy = (change.geometry.height - change.previous.height) * scale

              if (step == 0) {
                state.x -= dx
                state.y -= dy
                state.width -= sx
                state.height -= sy
              } else {
                state.x += dx / maxStep
                state.y += dy / maxStep
                state.width += sx / maxStep
                state.height += sy / maxStep
              }

              graph.cellRenderer.redraw(state)

              // Fades all connected edges and children
              mxEffects.cascadeOpacity(graph, change.cell, 100 * step / maxStep)
            }
          }
        }
      }

      if (step < maxStep && isRequired) {
        step++
        window.setTimeout(animate, delay)
      } else if (done != null) {
        done()
      }
    }

    var delay = 30
    animate()
  },

  /**
	 * Function: cascadeOpacity
	 *
	 * Sets the opacity on the given cell and its descendants.
	 *
	 * Parameters:
	 *
	 * graph - <mxGraph> that contains the cells.
	 * cell - <mxCell> to set the opacity for.
	 * opacity - New value for the opacity in %.
	 */
  cascadeOpacity: function (graph, cell, opacity) {
    // Fades all children
    var childCount = graph.model.getChildCount(cell)

    for (var i = 0; i < childCount; i++) {
      var child = graph.model.getChildAt(cell, i)
      var childState = graph.getView().getState(child)

      if (childState != null) {
        mxUtils.setOpacity(childState.shape.node, opacity)
        mxEffects.cascadeOpacity(graph, child, opacity)
      }
    }

    // Fades all connected edges
    var edges = graph.model.getEdges(cell)

    if (edges != null) {
      for (var i = 0; i < edges.length; i++) {
        var edgeState = graph.getView().getState(edges[i])

        if (edgeState != null) {
          mxUtils.setOpacity(edgeState.shape.node, opacity)
        }
      }
    }
  },

  /**
	 * Function: fadeOut
	 *
	 * Asynchronous fade-out operation.
	 */
  fadeOut: function (node, from, remove, step, delay, isEnabled) {
    step = step || 40
    delay = delay || 30

    var opacity = from || 100

    mxUtils.setOpacity(node, opacity)

    if (isEnabled || isEnabled == null) {
      var f = function () {
			    opacity = Math.max(opacity - step, 0)
        mxUtils.setOpacity(node, opacity)

        if (opacity > 0) {
          window.setTimeout(f, delay)
        } else {
          node.style.visibility = 'hidden'

          if (remove && node.parentNode) {
            node.parentNode.removeChild(node)
          }
        }
      }
      window.setTimeout(f, delay)
    } else {
      node.style.visibility = 'hidden'

      if (remove && node.parentNode) {
        node.parentNode.removeChild(node)
      }
    }
  }

}


var mxUtils = {

	errorResource: (mxClient.language != 'none') ? 'error' : '',
	closeResouce: (mxClient.language != 'none') ? 'error' : '',

	// Remove cursors - removes the cursors from the style of the given dom node and its descendants
	// element - DOM node to remove the cursor style from

	removeCursors: function (element) {
		if (element.style != null) {
			element.style.cursor = ''
		}
		var children = element.childNodes

		if (children != null) {
			var childCount = children.length
			for (var i = 0; i < childCount; i +=1) {
				mxUtils.removeCursors(children[i])
			}
		}
	},


	//Function - getcurrentstyle - returns the current style of the specified element
	//parameters - element - DOM node whose current style should be returned

	getCurrentStyle: (function () {
		if (mxClient.IS_IE && (document.documentMode == null || document.documentMode < 9)) {
			 return function (element) {
        return (element != null) ? element.currentStyle : null
      }
    } else {
      return function (element) {
        return (element != null)
          ? window.getComputedStyle(element, '')
          : null
      }
    }
  }()),

	//Function - Parse css number- parses the given CSS number value  adding handling for the value thin, medium and thick
	praseCssNumber: function (value) {
		if (value == 'thin') {
			value = '2'
		} else if (value == 'medium') {
			value = '4'
		} else if (value == 'thick') {
			value = '6'
		}

		value = praseFloat(value)

		if (isNaN(value)) {
			value = 0
		}
		return value
	}

	// FUnction - setPrefixedStyle
	// Adds the given style with standard name and optional vendor prefix for the current browser

	setPrefixedStyle: (function () {
    var prefix = null

    if (mxClient.IS_OT) {
      prefix = 'O'
    } else if (mxClient.IS_SF || mxClient.IS_GC) {
      prefix = 'Webkit'
    } else if (mxClient.IS_MT) {
      prefix = 'Moz'
    } else if (mxClient.IS_IE && document.documentMode >= 9 && document.documentMode < 10) {
      prefix = 'ms'
    }

    return function (style, name, value) {
      style[name] = value

      if (prefix != null && name.length > 0) {
        name = prefix + name.substring(0, 1).toUpperCase() + name.substring(1)
        style[name] = value
      }
    }
  }()),}

/** class - toolbar - creates a tool bar inside a DOM node. The toolbar may contain icon, buttons, comboboxes
	event - mxEvent.SELECT
	Fires when an item was selected in the toolbar. The <code>function</code> contains the function that was selected in <selectMode>
	Constructor - Mxtoobar
	Parameters - container - Dom node that contains the toolbar */


	function mxToolbar (container) {
		this.container = container
	};


	// extends mxEventsource
	mxToolbar.prototype = new mxEventSource()
	mxToolbar.prototype.constructor = mxToolbar

	// Variable - Constructor - Reference to the DOM node that contains the toolbar

	mxToolbar.prototype.container = null

	// Variable - enabled - specifies if events are handeled. Default is ture.

	mxToolbar.prototype.enabled = true

	// Variable - noreset - Specifies if <resetmode> requires a forcedflag of true for resetting the current mode in the toolbar.
	// Default is false. This is set to true if the toolbar item if the toolbar item is doubleclicked to avoid a reset after a single use of the item

	mxToolbar.prototype.noReset = false

	//Variable - updateDefaultmode- Boolean indicating if the deafult mode should be the last selected switch mode or first inserted switch mode.

	mxToolbar.prototype.updateDefaultmode = true

	// Function - addItem - Adds the given function as an image with specified title and Icon and returns a new image node
	// Parameters - Title - Optional string that is used as the tooltip
	// Parameters - icon - Optional url of the image to be used, if no url a button to be created.
	// parameters - funct - to execute on the mouse click 

	mxToolbar.prototype.addItem = function (title, icon, funct, pressedIcon, style, factoryMethod) {
		var img = document.createElement((icon != null) ? 'img' : 'button')
		var initialClassName = style || ((factoryMethod != null)
			? 'mxToolbarMode' : 'mxToolbarItem')
		img.className = initialClassName

		img.setAttribute('src', icon)

		if (title != null) {
			if (icon != null) {
				img.setAttribute('title', title)
			} else {
				mxUtils.write(img, title)
			}
		}

		this.container.appendChild(img)

		//Invokes the function onclick on the toolbar item

		if (funct != null) {
			mxEvent.addListener(img, 'click', funct)

			if (mxClient.IS_TOUCH) {
				mxEvent.addListener(img, 'touchend', funct)
			}
		}

		
	}





















console.log(mxClient)
