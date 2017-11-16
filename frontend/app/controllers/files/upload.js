import Controller from '@ember/controller';

export default Controller.extend({
  name: '',
  content: '',
  actions: {
    cancel: function() {
      this.set('name', '');
      this.set('content', '');
      this.transitionToRoute('files.index');
    },
    upload: function () {
      var name = this.get('name');
      var strippedName = name.replace(/^.*[\\/]/, '');
      var file = this.store.createRecord('file', {
        name: strippedName,
        content: this.get('content')
      });

      this.set('name', '');
      this.set('content', '');
      file.save();
      this.transitionToRoute('files');
    }
  }
});
