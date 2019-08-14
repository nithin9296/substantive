/** mxEventSource - base class for objects that dispatch named events. TO create a subclass that inherits from mxEventsSource, the following code is used

*/

function mxEventSource (eventSource) {
  this.setEventSource(eventSource)
};

// Variable - eventlisteners - Holds the event name and listeners in an array. The array contains the event name and listeners for each registered listener
mxEventSource.prototype.eventlisteners = null

// Variable- is enables- specifies if events can be fired. default is true
mxEventSource.prototype.eventsEnabled = true

// Variable - eventSource- Specifies if events can be fired. Default is true
mxEventSource.prototype.eventSource = null

// Function - isenabled - Returns <eventsenabled>

mxEventSource.prototype.isEventsEnabled = function () {
  return this.eventsenabled
}
// Function - setEventsEnabled

mxEventSource.prototype.setEventsEnabled = function (value) {
  this.eventsenabled = value
}

// getEventSource - Returns eventsource

mxEventSource.prototype.getEventSource = function () {
  return this.eventsource
}
// Function - setEventSource

mxEventSource.prototype.setEventSource = function (value) {
  this.eventsource = value
}

// Function - addListener - Binds the specified function to the given event name. If no event name is given, then the Listener is registered for all events

mxEventSource.prototype.addListener = function (name, funct) {
  if (this.eventlisteners == null) {
    this.eventlisteners = []
  }
  this.eventlisteners.push(name) // push() method adds new item to the end of an array.
  this.eventlisteners.push(funct)
}

// removeListener - Removes all the occurences of the given listener from <eventlistener>

mxEventSource.prototype.removeListener = function (funct) {
  if (this.eventlisteners != null) {
    var i = 0

    while (i < this.eventlisteners.length) {
      if (this.eventlisteners[i + 1] == funct) {
        this.eventlisteners.splice(i, 2) // Splice method adds/removes items to/from array
      } else {
        i += 2
      }
    }
  }
}

// Fireevent - dispatches the given event to the listeners which are registered for the event.

mxEventSource.prootype.fireEvent = function (evt, sender) {
  if (this.eventlisteners != null && this.isEventsEnabled()) {
    if (evt == null) {
      evt = new mxEventObject()
    }

    if (sender == null) {
      sender = this.getEventSource()
    }

    if (sender == null) {
    	sender = this
    }

    var args = [sender, evt]

    for (var i=0; i < this.eventlisteners.length; i += 2) {
    	var listen = this.eventlisteners[i]

    	if (listen == null || listen evt.getName()) {
    		this.eventlisteners[i + 1].apply(this, args)
    	}
    }

  }
}
