// 前端工作流

const gulp = require("gulp");

//转移jquery的文件
gulp.task("moveJquery", () => {
  return gulp
    .src("node_modules/jquery/dist/*.js")
    .pipe(gulp.dest("public/libs/jquery"));
});

