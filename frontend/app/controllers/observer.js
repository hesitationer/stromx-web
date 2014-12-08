import Ember from "ember";

import ParameterObserver from 'stromx-web/models/parameter-observer';
import InputObserver from 'stromx-web/models/input-observer';
import { Color } from 'stromx-web/controllers/stream';

export default Ember.ObjectController.extend({
  isEditing: false,
  
  visualizations: [
    {label: 'Default', value: 'default'},
    {label: 'Image', value: 'image_2d'}, 
    {label: 'Line segments', value: 'line_segments'},
    {label: 'Slider', value: 'slider'}
  ],
  
  visualizationLabel: function() {
    var visualization = this.get('visualization');
    
    var array = Ember.ArrayProxy.create({content: this.visualizations});
    var record = array.findBy('value', visualization);
    return record ? record['label'] : '';
  }.property('visualization'),

  title: function() {
    if (this.get('model') instanceof ParameterObserver) {
      return this.get('parameterTitle');
    } else if (this.get('model') instanceof InputObserver) {
      return this.get('inputTitle');
    } else {
      return '';
    }
  }.property('parameterTitle', 'inputTitle'),

  parameterTitle: function() {
    var parameter = this.get('parameter');
    var name = parameter.get('operator.name');
    var title = parameter.get('title');
    if (name) {
      title += " at " + name;
    }

    return title;
  }.property('parameter.title', 'parameter.operator.name'),

  inputTitle: function() {
    var input = this.get('input');
    var name = input.get('operator.name');
    var title = input.get('title');
    if (name) {
      title += " at " + name;
    }

    return title;
  }.property('input.title', 'input.operator.name'),

  actions: {
    edit: function() {
      this.set('isEditing', true);
    },
    
    save: function() {
      this.set('isEditing', false);
      var model = this.get('model');
      model.save();
    },
    
    moveUp: function() {
      var zvalue = this.get('zvalue');
      var model = this.get('model');
      this.get('view').then(function(view) {
        var observers = view.get('observers');
        var modelAbove = observers.findBy('zvalue', zvalue + 1);
        if (modelAbove) {
          model.set('zvalue', zvalue + 1);
          modelAbove.set('zvalue', zvalue);
          model.save();
          modelAbove.save();
        }
      });
    },

    moveDown: function() {
      var zvalue = this.get('zvalue');
      var model = this.get('model');
      this.get('view').then(function(view) {
        var observers = view.get('observers');
        var modelBelow = observers.findBy('zvalue', zvalue - 1);
        if (modelBelow) {
          modelBelow.set('zvalue', zvalue);
          model.set('zvalue', zvalue - 1);
          modelBelow.save();
          model.save();
        }
      });
    },

    setColor: function(key) {
      var model = this.get('model');
      var properties = model.get('properties');
      var color = Color[key];
      properties['color'] = color;
      model.set('properties', properties);
      model.save();
    },

    remove: function () {
      var observer = this.get('model');
      var zvalue = this.get('model.zvalue');
      var view = this.get('model.view');
      observer.deleteRecord();
      observer.save();

      view.then(function(view) {
        var observers = view.get('observers');
        observers.removeObject(observer);

        observers.then(function(observers) {
          observers.forEach(function(observer) {
            var thisZValue = observer.get('zvalue');
            if (thisZValue > zvalue) {
              observer.set('zvalue', thisZValue - 1);
            }
          });
        });
      });
    }
  }
});
