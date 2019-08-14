// Constructs a new Graph Editor

Menu = function (editorUi) {
  this.editorUi = editorUi
  this.menus = new Object()
  this.init()

  // Pre-fetches checkmark image

  if (!mxClient.IS_SVG) {
  	new Image().src = this.checkmarkImage
  }
}

// Set default font family

Menus.prototype.defaultFont = 'Helvetica'

// Set default font size

Menus.prototype.defaultFontSize = '12'

// Set menu items

Menus.prototype.defaultMenuItems = ['file', 'edit', 'view', 'arrange', 'extras', 'help']

Menus.prototype.defaultFonts = ['Helvetica', 'Verdana', 'Times New Roman', 'Garamond', 'Comic Sans MS',
           		             'Courier New', 'Georgia', 'Lucida Console', 'Tahoma']

Menus.prototype.init = function () {
  var graph = this.editorUi.editor.graph
  var isGraphEnabled = mxUtils.bind(graph, graph.isEnabled)

  this.put('fontFamily', new Menu(mxUtils.bind(this, function (menu, parent) {
    var addItem = mxUtils.bind(this, function (fontname) {
      var tr = this.styleChange(menu, fontname, [mxConstants.STYLE_FONTFAMILY], [fontname], null, parent, function () {
        document.execCommand('fontname', false, fontname)
      }, function () {

      })
    })
  })))
}
