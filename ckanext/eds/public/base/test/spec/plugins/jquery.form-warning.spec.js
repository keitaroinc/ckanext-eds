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

describe('jQuery.incompleteFormWarning()', function () {
  beforeEach(function () {
    this.el = jQuery('<form />').appendTo(this.fixture);
    this.el.on('submit', false);

    this.input1 = jQuery('<input name="input1" value="a" />').appendTo(this.el);
    this.input2 = jQuery('<input name="input2" value="b" />').appendTo(this.el);

    this.el.incompleteFormWarning('my message');

    this.on = sinon.stub(jQuery.fn, 'on');
    this.off = sinon.stub(jQuery.fn, 'off');
  });

  afterEach(function () {
    this.on.restore();
    this.off.restore();
  });

  it('should bind a beforeunload event when the form changes', function () {
    this.input1.val('c');
    this.el.change();

    assert.called(this.on);
  });

  it('should unbind a beforeunload event when a form returns to the original state', function () {
    this.input1.val('c');
    this.el.change();

    this.input1.val('a');
    this.el.change();

    assert.called(this.off); 
  });

  it('should unbind the beforeunload event when the form is submitted', function () {
    this.el.submit();

    assert.called(this.off); 
  });
});

