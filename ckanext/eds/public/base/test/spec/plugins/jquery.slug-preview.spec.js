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

/*globals describe it assert jQuery*/
describe('jQuery.fn.slugPreview()', function () {
  beforeEach(function () {
    this.element = jQuery('<div><input /></div>');
  });

  it('should return the preview element', function () {
    var target = this.element.slugPreview();
    assert.ok(target.hasClass('slug-preview'));
  });

  it('should restore the stack when .end() is called', function () {
    var target = this.element.slugPreview();
    assert.ok(target.end() === this.element);
  });

  it('should allow a prefix to be provided', function () {
    var target = this.element.slugPreview({prefix: 'prefix'});
    assert.equal(target.find('.slug-preview-prefix').text(), 'prefix');
  });

  it('should allow a placeholder to be provided', function () {
    var target = this.element.slugPreview({placeholder: 'placeholder'});
    assert.equal(target.find('.slug-preview-value').text(), 'placeholder');
  });

  it('should allow translations for strings to be provided', function () {
    var target = this.element.slugPreview({
      i18n: {'Edit': 'translated'}
    });
    assert.equal(target.find('button').text(), 'translated');
  });

  it('should set preview value to the initial value of the input', function () {
    var input = this.element.find('input').val('initial');
    var target = this.element.slugPreview();

    assert.equal(target.find('.slug-preview-value').text(), 'initial');
  });

  it('should update the preview value when the target input changes', function () {
    var target = this.element.slugPreview();
    var input = this.element.find('input').val('initial');

    input.val('updated').change();
    assert.equal(target.find('.slug-preview-value').text(), 'updated');
  });

  it('should hide the original element', function () {
    var target = this.element.slugPreview();
    assert.ok(this.element.css('display') === 'none');
  });

  it('should show the original element when Edit is clicked', function () {
    var target = this.element.slugPreview();
    target.find('button').click();
    assert.ok(this.element.css('display') === 'block');
  });

  it('should hide the preview element when Edit is clicked', function () {
    var target = this.element.slugPreview();
    target.find('button').click();
    assert.ok(target.css('display') === 'none');
  });
});

