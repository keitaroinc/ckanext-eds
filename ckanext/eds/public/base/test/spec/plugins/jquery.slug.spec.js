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

/*globals beforeEach describe it assert jQuery*/
describe('jQuery.fn.slug()', function () {
  beforeEach(function () {
    this.input = jQuery('<input />').slug();
    this.fixture.append(this.input);
  });

  it('should slugify and append the pressed key', function () {
    var e = jQuery.Event('keypress', {charCode: 97 /* a */});
    this.input.trigger(e);

    assert.equal(this.input.val(), 'a', 'append an "a"');

    e = jQuery.Event('keypress', {charCode: 38 /* & */});
    this.input.trigger(e);

    assert.equal(this.input.val(), 'a-', 'append an "-"');
  });

  it('should do nothing if a non character key is pressed', function () {
    var e = jQuery.Event('keypress', {charCode: 0});
    this.input.val('some other string').trigger(e);

    assert.equal(this.input.val(), 'some other string');
  });

  it('should slugify the input contents on "blur" and "change" events', function () {
    this.input.val('apples & pears').trigger(jQuery.Event('blur'));
    assert.equal(this.input.val(), 'apples-pears', 'on blur');

    this.input.val('apples & pears').trigger(jQuery.Event('change'));
    assert.equal(this.input.val(), 'apples-pears', 'on change');
  });
});

