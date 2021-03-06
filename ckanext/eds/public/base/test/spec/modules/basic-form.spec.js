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

/*globals describe beforeEach afterEach it assert sinon ckan jQuery */
describe('ckan.module.BasicFormModule()', function () {
  var BasicFormModule = ckan.module.registry['basic-form'];

  beforeEach(function () {
    sinon.stub(jQuery.fn, 'incompleteFormWarning');

    this.el = document.createElement('button');
    this.sandbox = ckan.sandbox();
    this.sandbox.body = this.fixture;
    this.module = new BasicFormModule(this.el, {}, this.sandbox);
  });

  afterEach(function () {
    this.module.teardown();
    jQuery.fn.incompleteFormWarning.restore();
  });

  describe('.initialize()', function () {
    it('should attach the jQuery.fn.incompleteFormWarning() to the form', function () {
      this.module.initialize();
      assert.called(jQuery.fn.incompleteFormWarning);
    });
  });
});

