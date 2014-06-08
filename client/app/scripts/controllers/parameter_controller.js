/* global App */

App.ParameterController = Ember.ObjectController.extend({  
  isEditing: false,
  
  isEnum: function() {
    return this.get('type') === 'enum';
  }.property('type'),
  
  isString: function() {
    return this.get('type') === 'string';
  }.property('type'),
  
  isInt: function() {
    return this.get('type') === 'int';
  }.property('type'),
  
  isFloat: function() {
    return this.get('type') === 'float';
  }.property('type'),
  
  isBool: function() {
    return this.get('type') === 'bool';
  }.property('type'),
  
  isTrigger: function() {
    return this.get('type') === 'trigger';
  }.property('type'),
  
  timedOut: function() {
    return this.get('state') === 'timedOut';
  }.property('state'),
  
  current: function() {
    return this.get('state') === 'current';
  }.property('state'),                                                        
                                                        
  editable: function() {
    var typeIsKnown = (this.get('isString') || 
                       this.get('isEnum') || 
                       this.get('isInt') || 
                       this.get('isFloat'));
    return this.get('writable') && this.get('current') && typeIsKnown;
  }.property('writable', 'isString', 'isInt', 'isFloat', 'state'),
                                                        
  writeOnly: Ember.computed.not('writable'),
                                                        
  accessFailed: function() {
    return this.get('state') === 'accessFailed';
  }.property('state'),
                                                        
  editValue:  function(key, value) {
    if (value === undefined) {
      if (this.get('isInt') || this.get('isFloat'))
        return this.get('numberValue');
      else if (this.get('isString'))
        return this.get('stringValue');
      else
        return '';
    }
    else {
      var v;
      if (this.get('isInt')) {
        v = parseInt(value, 10);
        this.set('numberValue', v);
        return v;
      }
      else if (this.get('isFloat')) {
        v = parseFloat(value);
        this.set('numberValue', v);
        return v;
      }
      else if (this.get('isString')) {
        this.set('stringValue', value);
        return value;
      }
    }
  }.property('stringValue', 'numberValue', 'type'),      
                                                        
  boolValue:  function(key, value) {
    if (value === undefined) {
      return this.get('numberValue') === 1;
    }
    else {
      var v = value ? 1 : 0;
      this.set('numberValue', v);
      var model = this.get('model');
      model.save();
      return value;
    }
  }.property('numberValue'),
                                                        
  displayValue: function(key, value) {
    if (value !== undefined)
      return value;
      
    if (! this.get('current'))
      return '';
    
    if (this.get('isEditing'))
      return '';
      
    if (this.get('isInt'))
      return this.get('numberValue');
    else if (this.get('isFloat'))
      return this.get('numberValue');
    else if (this.get('isEnum'))
      return this.updateEnumTitle(this.get('numberValue'));
    else 
      return this.get('stringValue');
      
  }.property('stringValue', 'numberValue', 'type', 'isEditing'),   
                                                        
  // cf. http://stackoverflow.com/q/20623027
  updateEnumTitle: function(enumValue) {
    var value = enumValue;
    var title = this.get('descriptions').then( function(value){
      return value.find( function(item, index, enumerable) {
         return item.get('value') === enumValue;
      });
    }).then( function(obj) {
      return obj.get('title');
    });
    
    var that = this;
    title.then( function(title) {
      that.set('displayValue', title);
      value = title;
    });
    
    return value;
  },
  
  actions: {
    editValue: function() {
      this.set('isEditing', true);
    }, 
    
    saveValue: function() {
      this.set('isEditing', false);
      var model = this.get('model');
      model.save();
    },
    
    reload: function() {
      var model = this.get('model');
      model.reload();
    },
    
    trigger: function() {
      this.set('numberValue', 1);
      var model = this.get('model');
      model.save();
    }
  }
});