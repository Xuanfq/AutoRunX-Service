

export const uploadFile = (filetype, callback) => {
    let input = document.createElement('input');
    input.type = 'file';
    input.accept = filetype;
    input.onchange = event => {
        let file = event.target.files[0];
        let file_reader = new FileReader();
        file_reader.onload = () => {
            let fc = file_reader.result;
            // console.log(fc); // 打印文件文本内容
            callback(fc)
        };
        file_reader.readAsText(file, 'UTF-8');
    };
    input.click();
}


export const downloadFile = (filename, data) => {
    var downloadElement = document.createElement('a');
    var href = window.URL.createObjectURL(new Blob([data], {
        type: "text/plain;charset=utf-8"
    }))
    downloadElement.href = href;
    downloadElement.download = filename;
    document.body.appendChild(downloadElement);
    downloadElement.click();
    document.body.removeChild(downloadElement);
    window.URL.revokeObjectURL(href);
}


/**
 * 将svg导出成图片
 * @param node svg节点 => document.querySelector('svg')
 * @param name 生成的图片名称
 * @param width 生成的图片宽度
 * @param height 生成的图片高度
 * @param type 生成的图片类型
 */
export const convertSVG2Image = (node, name, width, height, type = 'png') => {
    let serializer = new XMLSerializer()
    let source = '<?xml version="1.0" standalone="no"?>\r\n' + serializer.serializeToString(node)
    let image = new Image()
    image.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(source)
    console.log(image.src)
    let canvas = document.createElement('canvas')
    canvas.width = width
    canvas.height = height
    let context = canvas.getContext('2d')
    // context.fillStyle = '#fff'
    // context.fillRect(0, 0, 10000, 10000)
    image.onload = function () {
        context.drawImage(image, 0, 0, width, height)
        let a = document.createElement('a')
        a.download = `${name}.${type}`
        a.href = canvas.toDataURL(`image/${type}`, 1)
        a.click()
    }
}






















