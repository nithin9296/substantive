$(function () {
  /* Functions */

  var loadForm = function () {
    var btn = $(this)
    $.ajax({
      url: btn.attr('data-url'),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $('#client-modal-sample .modal-content').html('')
        $('#client-modal-sample').modal('show')
      },
      success: function (data) {
        $('#client-modal-sample .modal-content').html(data.html_form)
      }
    })
  }

  var saveForm = function () {
    var form = $(this)
    $.ajax({
      url: form.attr('action'),
      data: form.serialize(),
      type: form.attr('method'),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $('#client-sample-table tbody').html(data.html_object_list)
          $('#client-modal-sample').modal('hide')
        } else {
          $('#client-modal-sample .modal-content').html(data.html_form)
        }
      }
    })
    return false
  }

  /* Binding */

  // Create book
  // $('.js-create-book').click(loadForm)
  // $('#modal-book').on('submit', '.js-book-create-form', saveForm)

  // Update book
  $('#client-sample-table').on('click', '.js-client-update-sample', loadForm)
  $('#client-modal-sample').on('submit', '.js-client-sample-update-form', saveForm)

  // // Delete book
  // $('#book-table').on('click', '.js-delete-book', loadForm)
  // $('#modal-book').on('submit', '.js-book-delete-form', saveForm)
})
