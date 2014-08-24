/* global App */

App.ApplicationRoute = Ember.Route.extend({
  socket: null,

  activate: function() {
    var url = 'ws://' + window.location.host + '/error_socket';
    var ws = new WebSocket(url);
    var store = this.store;
    var controller = this;
    ws.onmessage = function(event) {
      var payload = JSON.parse(event.data);
      store.pushPayload('error', payload);
      Ember.run.next(function() {
        store.find('error', payload.error.id).then(function(error) {
          controller.pushObject(error);
        });
      });
    };
    this.set('socket', ws);
  },

  deactivate: function() {
    var ws = this.get('socket');
    ws.close();
  },

  actions: {
    showModal: function(modal, model) {
      var controller = this.controllerFor(modal);
      controller.set('model', model);
      return this.render(modal, {
        into: 'application',
        outlet: 'modal',
        controller: controller
      });
    },
    closeModal: function() {
      return this.disconnectOutlet({
        outlet: 'modal',
        parentView: 'application'
      });
    }
  }
});
