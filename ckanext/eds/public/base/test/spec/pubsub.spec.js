/*
Copyright (c) 2018 Keitaro AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

describe('ckan.pubsub', function () {
  beforeEach(function () {
    ckan.pubsub.events = jQuery({});
    ckan.pubsub.queue = [];
  });

  describe('.enqueue()', function () {
    beforeEach(function () {
      this.target = sinon.spy();
    });

    it('should defer callbacks for published events until later', function () {
      ckan.pubsub.subscribe('change', this.target);
      ckan.pubsub.enqueue();
      ckan.pubsub.publish('change');

      assert.notCalled(this.target);
    });

    it('should add the published calls to the .queue', function () {
      var queue = ckan.pubsub.queue;

      ckan.pubsub.enqueue();

      ckan.pubsub.publish('change');
      assert.equal(queue.length, 1);

      ckan.pubsub.publish('change');
      assert.equal(queue.length, 2);

      ckan.pubsub.publish('change');
      assert.equal(queue.length, 3);
    });
  });

  describe('.dequeue()', function () {
    beforeEach(function () {
      ckan.pubsub.queue = [
        ['change'],
        ['change', 'arg1', 'arg2'],
        ['update', 'arg1']
      ];

      this.target1 = sinon.spy();
      this.target2 = sinon.spy();
      this.target3 = sinon.spy();

      ckan.pubsub.subscribe('change', this.target1);
      ckan.pubsub.subscribe('change', this.target2);
      ckan.pubsub.subscribe('update', this.target3);
    });

    it('should publish all queued callbacks', function () {
      ckan.pubsub.dequeue();

      assert.calledTwice(this.target1);
      assert.calledWith(this.target1, 'arg1', 'arg2');

      assert.calledTwice(this.target2);
      assert.calledWith(this.target2, 'arg1', 'arg2');

      assert.calledOnce(this.target3);
    });

    it('should set the queue to null to allow new events to be published', function () {
      ckan.pubsub.dequeue();
      assert.isNull(ckan.pubsub.queue);
    });

    it('should not block new events from being published', function () {
      var pubsub = ckan.pubsub;

      var second = sinon.spy();
      var third  = sinon.spy();

      pubsub.enqueue();
      pubsub.subscribe('first', function () {
        pubsub.publish('third');
      });
      pubsub.subscribe('second', second);
      pubsub.subscribe('third', third);

      pubsub.publish('first');
      pubsub.publish('second');

      pubsub.dequeue();

      assert.called(second);
      assert.called(third);
    });
  });
});

