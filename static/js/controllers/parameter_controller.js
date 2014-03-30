App.ParameterController = Ember.ObjectController.extend({  
  isEditing: false,
  
  isEnum: function() {
    return this.get('type') == 'enum'
  }.property('type'),
  
  isString: function() {
    return this.get('type') == 'string'
  }.property('type'),
  
  isInt: function() {
    return this.get('type') == 'int'
  }.property('type'),
  
  isFloat: function() {
    return this.get('type') == 'float'
  }.property('type'),
  
  isBool: function() {
    return this.get('type') == 'bool'
  }.property('type'),
  
  isTrigger: function() {
    return this.get('type') == 'trigger'
  }.property('type'),
  
  timedOut: function() {
    return this.get('state') == 'timedOut'
  }.property('state'),
                                                        
  editable: function() {
    var typeIsKnown = (this.get('isEnum') || 
                       this.get('isString') || 
                       this.get('isInt') || 
                       this.get('isFloat'));
    return this.get('writable') && typeIsKnown
  }.property('writable', 'type'),
                                                        
  accessFailed: function() {
    return this.get('state') == 'accessFailed' || this.get('state') == 'timedOut'
  }.property('state'),
                                                        
  editValue:  function(key, value) {
    if (arguments.length > 1) {
      if (this.get('isInt')) {
        var v = parseInt(value)
        this.set('numberValue', v)
        return v
      }
      else if (this.get('isFloat')) {
        var v = parseFloat(value)
        this.set('numberValue', v)
        return v
      }
      else if (this.get('isString')) {
        this.set('stringValue', value)
        return value
      }
    }
    else {
      if (this.get('isInt') || this.get('isFloat'))
        return this.get('numberValue')
      else if (this.get('isString'))
        return this.get('stringValue')
      else
        return ''
    }
  }.property('stringValue', 'numberValue', 'type'),
  
  displayValue: function(key, value) {
    if (arguments.length > 1) {
      return value
    }
    
    if (this.get('isInt'))
      return this.get('numberValue')
    else if (this.get('isFloat'))
      return this.get('numberValue')
    else if (this.get('isBool'))
      return this.get('numberValue') == 0 ? 'False' : 'True'
    else if (this.get('isEnum'))
      return this.updateEnumTitle(this.get('numberValue'))
    else
      return this.get('stringValue')
  }.property('stringValue', 'numberValue', 'type'),
  
  // cf. http://stackoverflow.com/questions/20623027/rendering-resolved-promise-value-in-ember-handlebars-template
  updateEnumTitle: function(enumValue) {
    var value = enumValue
    var title = this.get('descriptions').then( function(value){
      return value.find( function(item, index, enumerable) {
         return item.get('value') == enumValue
      })
    }).then( function(obj) {
      return obj.get('title')
    })
    
    var that = this
    title.then( function(title) {
      that.set('displayValue', title)
      value = title
    })
    
    return value
  },
  
  actions: {
    editValue: function() {
      this.set('isEditing', true)
    }, 
    saveValue: function() {
      this.set('isEditing', false)
      var model = this.get('model')
      model.save()
    },
    reload: function() {
      var model = this.get('model')
      model.reload()
    },
    trigger: function() {
      this.set('numberValue', 1)
      var model = this.get('model')
      model.save()
    }
  }
});
