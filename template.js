function _canvas_auto_rubric(data) {

  const $inputs = $('input.criterion_points.span1.no-margin-bottom');
  const $submit_btn = $('.save_rubric_button');
  const $view_rubric_btn = $('.toggle_full_rubric');
  const $grade_input = $('#grading-box-extended');

  const update_score = function(data) {
    // const data = [8, 17, 15, 10, 5, 0, 16, 6, 10];
    let score = 0;

    $view_rubric_btn.click();

    for (let i = 0; i < data.length; i++) {
      $($inputs[i]).val(data[i]);
      score += parseInt(data[i]);
    }

    $submit_btn.click();
    $grade_input.val(score);
    $grade_input.change();

  };

  const $next_student_btn = $('i.icon-arrow-right.next');
  let student_set = new Set();

  const timer = setInterval(() => {
    $next_student_btn.click();

    const student_id = $('#avatar img').attr('src').match('[0-9]+')[0];
    // console.log(student_set);
    console.log(student_set.length, student_id);

    if (student_set.has(student_id)) {
      clearInterval(timer);
    }

    student_set.add(student_id);

    // const data = [8, 17, 15, 10, 5, 0, 16, 6, 10];
    if (data.hasOwnProperty(student_id)) {
      update_score(data[student_id]);
      console.log(data[student_id]);
    }

  }, 3000);

}
