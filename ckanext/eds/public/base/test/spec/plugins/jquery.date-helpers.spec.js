/*
Copyright (c) 2018 Keitaro AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

/*globals describe beforeEach afterEach it assert sinon ckan jQuery */
describe('jQuery.date', function () {
  beforeEach(function () {
    this.now = new Date();
    this.now.setTime(0);

    this.clock = sinon.useFakeTimers(this.now.getTime());
  });

  afterEach(function () {
    this.clock.restore();
  });

  describe('jQuery.date.format()', function () {
    it('should format the date based on the string provided', function () {
      var target = jQuery.date.format('yyyy-MM-dd', this.now);
      assert.equal(target, '1970-01-01');
    });

    it('should use the current time if none provided', function () {
      var target = jQuery.date.format('yyyy/MM/dd');
      assert.equal(target, '1970/01/01');
    });
  });

  describe('jQuery.date.toISOString()', function () {
    it('should output an ISO8601 compatible string', function () {
      var target = jQuery.date.toISOString(this.now);
      assert.equal(target, '1970-01-01T00:00:00.000Z');
    });

    it('should use the current time if none provided', function () {
      var target = jQuery.date.toISOString();
      assert.equal(target, '1970-01-01T00:00:00.000Z');
    });
  });
});
