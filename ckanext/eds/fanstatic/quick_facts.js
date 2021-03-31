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

(function () {
  'use strict';
  var api = {
    get: function (action, params) {
      var api_ver = 3;
      var base_url = ckan.sandbox().client.endpoint;
      params = $.param(params);
      var url = base_url + '/api/' + api_ver + '/action/' + action + '?' + params;
      return $.getJSON(url);
    },
    post: function (action, data) {
      var api_ver = 3;
      var base_url = ckan.sandbox().client.endpoint;
      var url = base_url + '/api/' + api_ver + '/action/' + action;
      return $.post(url, JSON.stringify(data), "json");
    }
  };

  $(document).ready(function () {

    // Fetch and populate datasets dropdowns

    api.get('eds_show_datasets', {}).done(function (data) {
      var inputs = $('[id*=chart_dataset_]');
      $.each(data.result, function (idx, elem) {
        inputs.append(new Option(elem.title, elem.name));
      });

      // Dataset event handlers
      var dataset_name;
      inputs.on('change', function () {
        var elem = $(this);
        dataset_name = elem.find(":selected").val();
        var dataset_select_id = elem.attr('id');
        var resource_select_id = dataset_select_id.replace('dataset', 'resource');
        var resourceview_select_id = resource_select_id.replace('resource', 'resource_view');

        // Empty all child selects
        if ($('#' + resource_select_id + ' option').length > 0)
          $('#' + resource_select_id).find('option').not(':first').remove();

        $('#' + resource_select_id).prop('required', 'required');
        $('#' + resourceview_select_id + '_preview').empty();

        // Fetch and populate resources drop down
        api.get('eds_dataset_show_resources', {
          id: dataset_name
        }).done(
          function (data) {
            var opts = $('#' + resource_select_id);
            $.each(data.result, function (idx, elem) {
              var name;

              if (elem.name) {
                name = elem.name;
              } else if (elem.description) {
                name = elem.description;
              } else {
                name = 'Unnamed resource';
              }

              opts.append(new Option(name, elem.id));
            });

            $('.' + resource_select_id).removeClass('hidden');
          });
      });

      // Resource event handlers

      var resource_id;
      var resource_inputs = $('[id*=chart_resource_]');
      resource_inputs.on('change', function () {

        var elem = $(this);
        resource_id = elem.find(":selected").val();
        var resource_select_id = elem.attr('id');
        var resourceview_select_id = resource_select_id.replace('resource', 'resourceview');

        if ($('#' + resourceview_select_id + ' option').length > 0)
          $('#' + resourceview_select_id).find('option').not(':first').remove();

        $('#' + resourceview_select_id).prop('required', 'required');
        $('#' + resourceview_select_id + '_preview').html();

        api.get('eds_resource_show_resource_views', {
          id: resource_id,
          view_type: 'Chart builder'
        }).done(
          function (data) {

            var opts = $('#' + resourceview_select_id);
            $.each(data.result, function (idx, elem) {
              opts.append(new Option(elem.title, elem.id));
            });

            $('.' + resourceview_select_id).removeClass('hidden');
          });
      });

      // Resource views event handlers

      var resourceview_inputs = $('[id*=chart_resourceview_]');
      resourceview_inputs.on('change', function () {

        var elem = $(this);
        var resourceview_id = elem.find(":selected").val();

        var resourceview_select_id = elem.attr('id');
        var chart_nr = resourceview_select_id.substr(resourceview_select_id.lastIndexOf('_') + 1);

        $('#ckanext\\.eds\\.chart_' + chart_nr).val(resourceview_id)

        var base_url = ckan.sandbox().client.endpoint;
        var src = base_url + '/dataset/' + dataset_name + '/resource/' + resource_id + '/view/' + resourceview_id;

        ckan.sandbox().client.getTemplate('iframe.html', {
            source: src
          })
          .done(function (data) {

            $('#' + resourceview_select_id + '_preview').html();
            $('#' + resourceview_select_id + '_preview').html(data);
            $('#' + resourceview_select_id + '_preview').removeClass('hidden');

          });

          $('#submit_button_' + chart_nr).show();
      });

      // Change chart buttons event handlers

      var change_chart_buttons = $('[id*=change_chart_button_]');
      change_chart_buttons.on('click', function (e) {
        e.preventDefault();

        var elem = $(this);
        var change_button_id = elem.attr('id');
        var chart_nr = change_button_id.substr(change_button_id.lastIndexOf('_') + 1);

        $('#edit_buttons_' + chart_nr).addClass('hidden');
        $('#change_chart_' + chart_nr).removeClass('hidden');
        $('#submit_button_' + chart_nr).show();

      });

      // Clear chart buttons event handlers

      var clear_chart_buttons = $('[id*=clear_chart_]');
      clear_chart_buttons.on('click', function (e) {
        e.preventDefault();

        var elem = $(this);
        var clear_button_id = elem.attr('id');
        var chart_nr = clear_button_id.substr(clear_button_id.lastIndexOf('_') + 1);

        $('#ckanext\\.eds\\.chart_' + chart_nr).val('')
        $('#chart_resourceview_' + chart_nr + '_preview').addClass('hidden');
        $('#edit_buttons_' + chart_nr).addClass('hidden');
        $('#change_chart_' + chart_nr).removeClass('hidden');
        $('#submit_button_' + chart_nr).show();

      });

    });

  });
})($);