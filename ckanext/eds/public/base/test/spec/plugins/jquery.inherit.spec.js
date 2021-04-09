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
describe('jQuery.inherit()', function () {
  beforeEach(function () {
    this.MyClass = function MyClass() {};
    this.MyClass.static = function () {};
    this.MyClass.prototype.method = function () {};
  });

  it('should create a subclass of the constructor provided', function () {
    var target = new (jQuery.inherit(this.MyClass))();
    assert.isTrue(target instanceof this.MyClass);
  });

  it('should set the childs prototype object', function () {
    var target = new (jQuery.inherit(this.MyClass))();
    assert.isFunction(target.method);
  });

  it('should copy over the childs static properties', function () {
    var Target = jQuery.inherit(this.MyClass);
    assert.isFunction(Target.static);
  });

  it('should allow instance properties to be overridden', function () {
    function method() {}

    var target = new (jQuery.inherit(this.MyClass, {method: method}))();
    assert.equal(target.method, method);
  });

  it('should allow static properties to be overridden', function () {
    function staticmethod() {}

    var Target = jQuery.inherit(this.MyClass, {}, {static: staticmethod});
    assert.equal(Target.static, staticmethod);
  });

  it('should allow a custom constructor to be provided', function () {
    var MyConstructor = sinon.spy();
    var Target = jQuery.inherit(this.MyClass, {constructor: MyConstructor});

    new Target();

    sinon.assert.called(MyConstructor);
  });
});

