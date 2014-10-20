/* global App */

App.Connection = DS.Model.extend({
  sourceConnector: DS.belongsTo('connector', {async: true}),
  targetConnector: DS.belongsTo('connector', {async: true}),
  thread: DS.belongsTo('thread', {async: true}),
  stream: DS.belongsTo('stream', {async: true})
});

App.Connection.FIXTURES = [
  {
    id: 1,
    sourceConnector: 5,
    targetConnector: 2,
    thread: 1,
    stream: 2
  },
  {
    id: 2,
    sourceConnector: 5,
    targetConnector: 3,
    thread: null,
    stream: 2
  }
];
