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
describe('ckan.notify()', function () {
  beforeEach(function () {
    this.element = jQuery('<div />');
    this.fixture.append(this.element);

    ckan.notify.el = this.element;
  });

  it('should append a notification to the element', function () {
    ckan.notify('test');
    assert.equal(this.element.children().length, 1, 'should be one child');
    ckan.notify('test');
    assert.equal(this.element.children().length, 2, 'should be two children');
  });

  it('should append a notification title', function () {
    ckan.notify('test');
    assert.equal(this.element.find('strong').text(), 'test');
  });

  it('should append a notification body', function () {
    ckan.notify('test', 'this is a message');
    assert.equal(this.element.find('span').text(), 'this is a message');
  });

  it('should escape all content', function () {
    ckan.notify('<script>', '<script>');
    assert.equal(this.element.find('strong').html(), '&lt;script&gt;');
    assert.equal(this.element.find('span').html(), '&lt;script&gt;');
  });

  it('should default the class to "alert-error"', function () {
    ckan.notify('test');
    assert.ok(this.element.find('.alert').hasClass('alert-error'));
  });

  it('should allow a type to be provided', function () {
    ckan.notify('test', '', 'info');
    assert.ok(this.element.find('.alert').hasClass('alert-info'));
  });

  it('should add itself to the ckan.sandbox()', function () {
    assert.equal(ckan.sandbox().notify, ckan.notify);
  });
});
