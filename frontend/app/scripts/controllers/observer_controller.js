/* global App */

App.ObserverController = Ember.ObjectController.extend({
  visualizationLabel: function() {
    var visualization = this.get('visualization');

    if (visualization === 'image')
      return 'Image';
    else if (visualization === 'lines')
      return 'Lines';
    else if (visualization === 'slider')
      return 'Slider';
    else if (visualization === 'default')
      return 'Default';
    else
      return '';
  }.property('visualization'),

  title: function() {
    if (this.get('model') instanceof App.ParameterObserver)
      return this.get('parameterTitle');
    else if (this.get('model') instanceof App.InputObserver)
      return this.get('inputTitle');
    else
      return '';
  }.property('parameterTitle', 'inputTitle'),

  parameterTitle: function() {
    var parameter = this.get('parameter');
    var name = parameter.get('operator.name');
    var title = parameter.get('title');
    if (name)
      title += " at " + name;
    
    return title;
  }.property('parameter.title', 'parameter.operator.name'),

  inputTitle: function() {
    var input = this.get('input');
    var name = input.get('operator.name');
    var title = input.get('title');
    if (name)
      title += " at " + name;
    
    return title;
  }.property('input.title', 'input.operator.name'),

  actions: {
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
            if (thisZValue > zvalue)
              observer.set('zvalue', thisZValue - 1);
          });
        });
      });
    }
  }
});
