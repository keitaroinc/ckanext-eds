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
describe('jQuery.url', function () {
  describe('.escape()', function () {
    it('should escape special characters', function () {
      var target = jQuery.url.escape('&<>=?#/');
      assert.equal(target, '%26%3C%3E%3D%3F%23%2F');
    });

    it('should convert spaces to + rather than %20', function () {
      var target = jQuery.url.escape(' ');
      assert.equal(target, '+');
    });
  });

  describe('.slugify()', function () {
    it('should replace spaces with hyphens', function () {
      var target = jQuery.url.slugify('apples and pears');
      assert.equal(target, 'apples-and-pears');
    });

    it('should lowecase all characters', function () {
      var target = jQuery.url.slugify('APPLES AND PEARS');
      assert.equal(target, 'apples-and-pears');
    });

    it('should convert unknown characters to hyphens', function () {
      var target = jQuery.url.slugify('apples & pears');
      assert.equal(target, 'apples-pears');
    });

    it('should nomalise hyphens', function () {
      var target = jQuery.url.slugify('apples---pears');
      assert.equal(target, 'apples-pears', 'remove duplicate hyphens');

      target = jQuery.url.slugify('--apples-pears');
      assert.equal(target, 'apples-pears', 'strip preceding hyphens');

      target = jQuery.url.slugify('apples-pears--');
      assert.equal(target, 'apples-pears', 'strip trailing hyphens');
    });

    it('should try and asciify unicode characters', function () {
      var target = jQuery.url.slugify('éåøç');
      assert.equal(target, 'eaoc');
    });
  });
});

