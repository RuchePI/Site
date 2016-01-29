"use strict";

var gulp = require("gulp"),
    path = require("path"),
    del = require("del"),
    $ = require("gulp-load-plugins")();

var paths = {
    sourceDir: "assets",
    sassDir: "scss",
    scriptsDir: "js",
    fontsDir: "fonts",
    vendorsDir: "vendors",
    stylesFiles: "main.scss",
    vendorsCSS: [
        "node_modules/normalize.css/normalize.css",
        "node_modules/font-awesome/css/font-awesome.css"
    ],
    vendorsJS: [
        "node_modules/jquery/dist/jquery.js",
        "node_modules/highcharts/highcharts.src.js",
        "node_modules/highcharts/modules/exporting.src.js"
    ],
    vendorsFonts: [
        "node_modules/font-awesome/fonts/*"
    ]
};

/* Cleans up the workspace, deletes the build. */
gulp.task("clean", function () {
    del([
        path.join(paths.sourceDir, paths.sassDir, paths.vendorsDir),
        path.join(paths.sourceDir, paths.scriptsDir, paths.vendorsDir)
    ]);
});

/* Copy vendors style files. */
gulp.task("vendors-css", function () {
    gulp.src(paths.vendorsCSS)
        .pipe($.rename({
            prefix: "_",
            extname: ".scss"
        }))
        .pipe(gulp.dest(path.join(paths.sourceDir, paths.sassDir, paths.vendorsDir)));
});

/* Compile SASS file. */
gulp.task("stylesheet", ["vendors-css"], function () {
    gulp.src(path.join(paths.sourceDir, paths.sassDir, paths.stylesFiles))
        .pipe($.sass())
        .on("error", $.notify.onError({
            title: "SASS Error",
            message: "Line <%= error.lineNumber %>: <%= error.message %>"
        }))
        .pipe($.autoprefixer({
            browser: ["last 1 version", "> 1%", "ff >= 20", "ie >= 8", "opera >= 12", "Android >= 2.2"],
            cascade: true
        }))
        .pipe(gulp.dest(path.join(paths.sourceDir, "css/")))
        .pipe($.rename({ suffix: ".min" }))
        .pipe($.minifyCss())
        .pipe(gulp.dest(path.join(paths.sourceDir, "css/")))
        .pipe($.livereload());
});

/* Copy fonts files. */
gulp.task("vendors-fonts", function () {
    gulp.src(paths.vendorsFonts)
        .pipe(gulp.dest(path.join(paths.sourceDir, paths.fontsDir)));
});

/* Copy vendors script fules. */
gulp.task("vendors-js", function () {
    gulp.src(paths.vendorsJS)
        .pipe(gulp.dest(path.join(paths.sourceDir, paths.scriptsDir, paths.vendorsDir)));
});

/* Scripts concat and minify. */
gulp.task("scripts", ["vendors-js"], function () {
    gulp.src([
        /* The order is critical! */
        path.join(paths.sourceDir, paths.scriptsDir, "vendors/{jquery,highcharts.src,exporting.src}.js"),
        path.join(paths.sourceDir, paths.scriptsDir, "*.js"),
        "!" + path.join(paths.sourceDir, paths.scriptsDir, "{all,all.min}.js")
    ])
        .pipe($.concat("all.js", { newLine: "\r\n\r\n" }))
        .pipe(gulp.dest(path.join(paths.sourceDir, paths.scriptsDir)))
        .pipe($.rename({ suffix: ".min" }))
        .pipe($.uglify().on("error", $.notify.onError({
            title: "Javascript Error",
            message: "<%= error.message %>"
        })))
        .pipe(gulp.dest(path.join(paths.sourceDir, paths.scriptsDir)));
});

/* Watch to recompiles and run LiveReload. */
gulp.task("watch", function () {
    gulp.watch([
        path.join(paths.sourceDir, paths.scriptsDir, "*.js"),
        "!" + path.join(paths.sourceDir, paths.scriptsDir, "vendors/*.js"),
        "!" + path.join(paths.sourceDir, paths.scriptsDir, "{all,all.min}.js")
    ], ["scripts"]);
    gulp.watch([
        path.join(paths.sourceDir, paths.sassDir, "**/*.scss"),
        "!" + path.join(paths.sourceDir, paths.sassDir, "vendors/*.scss")
    ], ["stylesheet"]);

    gulp.watch(["*"])
        .on("change", function (event) {
            $.livereload.changed(event.path);
        });

    $.livereload.listen();
});

/* Build all the things. */
gulp.task("build", ["vendors-fonts", "scripts", "stylesheet"]);

/* Default task: build and watch. */
gulp.task("default", ["build", "watch"]);
