const { src, dest, series } = require('gulp');
const rename = require('gulp-rename');
const path = require('path');
const print = require('gulp-print').default;

// styles
const scss = require('gulp-sass')(require('sass'));
const autoPrefixer = require('gulp-autoprefixer');
const cssMinify = require('gulp-clean-css');

function styles_scss(file, save_to, browser_sync) {
    src(file)
        .pipe(scss())
        .on('error', swallowError)
        .pipe(autoPrefixer('last 2 versions'))
        .on('error', swallowError)
        .pipe(cssMinify())
        .on('error', swallowError)
        .pipe(rename(path.basename(save_to)))
        .pipe(dest(path.dirname(save_to)))
        .pipe(browser_sync.stream());
}

// scripts
const jsMinify = require('gulp-terser');
function scripts(file, save_to, browser_sync) {
    src(file)
        .pipe(jsMinify())
        .on('error', swallowError)
        .pipe(rename(path.basename(save_to)))
        .pipe(dest(path.dirname(save_to)))
        .pipe(browser_sync.stream());
}

function copy(file, save_to, browser_sync) {
    src(file)
        .pipe(rename(path.basename(save_to)))
        .pipe(dest(path.dirname(save_to)))
        .pipe(browser_sync.stream());
}

// lesscss
const less = require('gulp-less');
function styles_less(file, save_to, browser_sync) {
    src(file)
        .pipe(less())
        .on('error', swallowError)
        .pipe(autoPrefixer('last 2 versions'))
        .on('error', swallowError)
        .pipe(cssMinify())
        .on('error', swallowError)
        .pipe(rename(path.basename(save_to)))
        .pipe(dest(path.dirname(save_to)))
        .pipe(browser_sync.stream());
}

const webp = require('gulp-webp');
const imagemin = require('gulp-imagemin');
function images(file, save_to, browser_sync) {
    console.log(`Images: ${save_to}`);
    src(file)
        .pipe(imagemin())
        .pipe(webp())
        .pipe(rename(path.basename(save_to)))
        .pipe(dest(path.dirname(save_to)))
        .pipe(browser_sync.reload({stream: true}));
}

const htmlmin = require('gulp-htmlmin');
function min_html(file, save_to, browser_sync) {
    src(file)
        .pipe(htmlmin({ collapseWhitespace: true }))
        .pipe(rename(path.basename(save_to)))
        .pipe(dest(path.dirname(save_to)))
        .pipe(browser_sync.stream());
}

function swallowError (error) {
    // If you want details of the error in the console
    console.log(error.toString())
    this.emit('end')
}

const files_map = {
    'js':     ['js',  scripts],
    'less':   ['css',  styles_less],
    'scss':   ['css',  styles_scss],
    'html':   ['html', min_html],

    'png':   ['webp',  images],
    'jpg':   ['webp',  images],
    'jpeg':   ['webp',  images],
    'bmp':   ['webp',  images],
    'webp':   ['webp',  copy],
};

module.exports.files_map = files_map;