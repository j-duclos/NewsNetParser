// Include gulp
let gulp = require('gulp');

// Include plugins
let touch = require('gulp-touch-cmd');
let notify = require('gulp-notify');

function wsgi_touch() {
  return (
    gulp.src('core/wsgi.py')
      .pipe(touch())
      .pipe(gulp.dest('core/wsgi.py'))
      .pipe(notify({ message: 'wsgi refresh complete' }))
  );
}

function watch(){
  gulp.watch(['NewsNetParser/*.*', 'NewsReleases/*.*', 'simplecache/*.*'], wsgi_touch);
}

exports.watch = watch;
exports.default = watch;