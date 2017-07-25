import { test } from 'qunit';
import moduleForAcceptance from 'stromx-web/tests/helpers/module-for-acceptance';

moduleForAcceptance('Acceptance: Connections');

test('visit connection', function(assert) {
  visit('/streams/2/connections/2');

  andThen(function() {
    assert.equal(
      currentRouteName(),
      'connection.index',
      'The connections is shown'
    );
  });
});

test('remove connection', function(assert) {
  visit('/streams/2/connections/2/delete');
  click('.stromx-accept');

  andThen(function() {
    assert.equal(
      find('.stromx-svg-connection-path').length,
      1,
      'Only one connection is shown'
    );
    assert.equal(
      currentRouteName(),
      'stream.index',
      'After removing the connection the stream is shown'
    );
  });
});

test('cancel removing connection', function(assert) {
  visit('/streams/2/connections/2/delete');
  click('.stromx-cancel');

  andThen(function() {
    assert.equal(
      find('.stromx-svg-connection-path').length,
      2,
      'Two connections are shown'
    );
    assert.equal(
      currentRouteName(),
      'connection.index',
      'After cancelling the connection is shown'
    );
  });
});

test('add connection output -> input', function(assert) {
  visit('/streams/2');
  triggerEvent('a[href="/streams/2/operators/0"] + g.stromx-svg-output g',
               'mousedown');
  triggerEvent('a[href="/streams/2/operators/2"] + g.stromx-svg-input g',
               'mouseover');
  triggerEvent('a[href="/streams/2/operators/0"] + g.stromx-svg-output g',
               'mouseup');

  andThen(function() {
    assert.equal(
      find('.stromx-svg-connection-path').length,
      3,
      'Three connections are shown'
    );
    assert.equal(
      currentRouteName(),
      'connection.index',
      'After adding a connection it is shown'
    );
  });
});

test('add connection input -> output', function(assert) {
  visit('/streams/2');
  triggerEvent('a[href="/streams/2/operators/2"] + g.stromx-svg-input g',
               'mousedown');
  triggerEvent('a[href="/streams/2/operators/0"] + g.stromx-svg-output g',
               'mouseover');
  triggerEvent('a[href="/streams/2/operators/2"] + g.stromx-svg-input g',
               'mouseup');

  andThen(function() {
    assert.equal(
      find('.stromx-svg-connection-path').length,
      3,
      'Three connections are shown'
    );
    assert.equal(
      currentRouteName(),
      'connection.index',
      'After adding a connection it is shown'
    );
  });
});

test('remove and add connection', function(assert) {
  visit('/streams/2/connections/2/delete');
  click('.stromx-accept');

  triggerEvent('a[href="/streams/2/operators/0"] + g.stromx-svg-output g',
               'mousedown');
  triggerEvent('a[href="/streams/2/operators/2"] + g.stromx-svg-input g',
               'mouseover');
  triggerEvent('a[href="/streams/2/operators/0"] + g.stromx-svg-output g',
               'mouseup');

  andThen(function() {
    assert.equal(find('.stromx-svg-connection-path').length, 2,
                 'Two connections are shown');
  });
});
