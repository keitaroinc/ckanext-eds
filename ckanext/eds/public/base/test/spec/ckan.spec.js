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

describe('ckan.initialize()', function () {
  beforeEach(function () {
    this.promise = jQuery.Deferred();
    this.target = sinon.stub(ckan.Client.prototype, 'getLocaleData').returns(this.promise);
  });

  afterEach(function () {
    this.target.restore();
  });

  it('should load the localisations for the current page', function () {
    ckan.initialize()
    assert.called(this.target);
  });

  it('should load the localisations into the i18n library', function () {
    var target = sinon.stub(ckan.i18n, 'load');
    var data = {lang: {}};

    ckan.initialize();
    this.promise.resolve(data);

    assert.called(target);
    assert.calledWith(target, data);

    target.restore();
  });

  it('should initialize the module on the page', function () {
    var target = sinon.stub(ckan.module, 'initialize');

    ckan.initialize();
    this.promise.resolve();

    assert.called(target);
    target.restore();
  });
});

describe('ckan.url()', function () {
  beforeEach(function () {
    ckan.SITE_ROOT = 'http://example.com';
    ckan.LOCALE_ROOT = ckan.SITE_ROOT + '/en';
  });

  it('should return the ckan.SITE_ROOT', function () {
    var target = ckan.url();
    assert.equal(target, ckan.SITE_ROOT);
  });

  it('should return the ckan.LOCALE_ROOT if true is passed', function () {
    var target = ckan.url(true);
    assert.equal(target, ckan.LOCALE_ROOT);
  });

  it('should append the path provided', function () {
    var target = ckan.url('/test.html');
    assert.equal(target, ckan.SITE_ROOT + '/test.html');
  });

  it('should append the path to the locale provided', function () {
    var target = ckan.url('/test.html', true);
    assert.equal(target, ckan.LOCALE_ROOT + '/test.html');
  });

  it('should handle missing preceding slashes', function () {
    var target = ckan.url('test.html');
    assert.equal(target, ckan.SITE_ROOT + '/test.html');
  });
});

