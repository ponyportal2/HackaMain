const { src, dest, series, watch } = require('gulp');
const path = require('path');
const fs = require('fs');

const browser_sync = require('browser-sync').create();

const { files_map } = require('./gulp_tasks/tasks');

const config = {
    from: 'src/',
    to: 'dist/',
};

function sanitize_path(filepath) {
    return filepath.replaceAll('\\', '/');
}

function file_extension(filename) {
    return filename.split('.').pop();
}

function replace_extension(filename, new_extension) {
    // Find index of last '.' in filename
    const dotIndex = filename.lastIndexOf('.');

    // Check if dot exists and it's not the first character in the filename
    if (dotIndex > 0) {
        return `${filename.slice(0, dotIndex)}.${new_extension}`;
    } else {
        return `${filename}.${new_extension}`;
    }
}

function replace_root_directory(filepath, oldRoot, newRoot) {
    const rootRegex = new RegExp(`^${oldRoot}`);
    if (rootRegex.test(filepath)) {
        return filepath.replace(rootRegex, newRoot);
    } else {
        return undefined;
    }
}

function get_last_modified_time(filepath) {
    return fs.statSync(filepath).mtime;
}

function file_exists(filepath) {
    return fs.existsSync(filepath);
}

function get_dist_filepath(src_filepath) {
    src_filepath = sanitize_path(src_filepath);
    const extension = file_extension(src_filepath);
    const tuple = files_map[extension];

    let dist_filepath = src_filepath;
    if (tuple !== undefined) {
        const [end_extension, callback] = tuple;
        dist_filepath = replace_extension(src_filepath, end_extension);
    }
    dist_filepath = replace_root_directory(dist_filepath, config.from, config.to);
    return dist_filepath;
}

const get_all_files_raw = function(dirPath, arrayOfFiles) {
    try {
        files = fs.readdirSync(dirPath);
    } catch (error) {
        return [];
    }
  
    arrayOfFiles = arrayOfFiles || []
  
    files.forEach(function(file) {
      if (fs.statSync(dirPath + "/" + file).isDirectory()) {
        arrayOfFiles = get_all_files_raw(dirPath + "/" + file, arrayOfFiles)
      } else {
        arrayOfFiles.push(path.join(__dirname, dirPath, "/", file))
      }
    })
  
    return arrayOfFiles;
}

const get_all_files = function(dir_path) {
    return get_all_files_raw(dir_path)
        .map(file => sanitize_path(path.normalize(file)))    
        .map(file => path.relative(sanitize_path(__dirname), file))
        .map(file => sanitize_path(file));
}

function fileChanged(filename, browser_sync) {
    filename = sanitize_path(filename);
    const extension = file_extension(filename);

    if (extension == 'pdnSave') {
        return;
    }

    const tuple = files_map[extension];
    let final_name = get_dist_filepath(filename);

    let update = false;
    if (file_exists(final_name))
        update = get_last_modified_time(filename) > get_last_modified_time(final_name);
    else
        update = true;

    if (!update)
        return;

    console.log(`Updating ${filename} -> ${final_name}`);
    if (tuple === undefined) {
        src(filename)
            .pipe(dest(path.dirname(final_name)))
            .pipe(browser_sync.stream());
    } else {
        const [end_extension, callback] = tuple;
        callback(filename, final_name, browser_sync);
    }
}

function fileDeleted(filename) {
    try {
        fs.unlinkSync(get_dist_filepath(filename));
    } catch (err) {}
    console.log(`File ${filename} deleted`);
}

function watchTask() {
    let src_path = `${config.from}**/*.*`;
    let all_files = get_all_files(config.from);
    let reachable_files = all_files.map(file => get_dist_filepath(file));

    let dist_files = get_all_files(config.to);
    for (let i = 0; i < dist_files.length; i++) {
        if (!reachable_files.includes(dist_files[i])) {
            try {
                fs.unlinkSync(dist_files[i]);
            } catch (err) {}
        }
    }

    browser_sync.init({
        server: {
            baseDir: config.to,
        }
    });

    all_files.forEach(file => fileChanged(file, browser_sync));

    let watcher = watch(src_path, { ignoreInitial: false });
    
    watcher.on('change', fileEvent => fileChanged(fileEvent.toString(), browser_sync));
    watcher.on('add', fileEvent => fileChanged(fileEvent.toString(), browser_sync));
    watcher.on('unlink', fileEvent => {
        fileDeleted(fileEvent.toString());
        browser_sync.reload();
    });
}

exports.default = series(watchTask);
