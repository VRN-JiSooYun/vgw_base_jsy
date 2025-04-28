var Size = Quill.import('attributors/style/size');

let quillSizeList = [];
let quillSizeStyle = document.createElement('style');
let quillStyleText = '';
for (var i = 8; i <= 24; i += 2) {
    quillSizeList.push(i + 'px');

    quillStyleText += `
        .ql-snow .ql-picker.ql-size .ql-picker-item[data-value="${i}px"]::before {
            content: attr(data-value);
            font-size: ${i}px !important;
        }
    `;
}

quillSizeStyle.innerText = quillStyleText;

document.head.appendChild(quillSizeStyle);

Size.whitelist = quillSizeList;
Quill.register(Size, true);
Quill.register("modules/imageCompressor", imageCompressor);
Quill.register("modules/resize", window.QuillResizeModule);

class QuillWrapper {
    constructor(targetDivId, targetInputId, quillOptions) {
        this.targetDiv = document.getElementById(targetDivId);
        if (!this.targetDiv) throw 'Target div(' + targetDivId + ') id was invalid';

        this.targetInput = document.getElementById(targetInputId);
        if (!this.targetInput) throw 'Target Input id was invalid';

        // quillOptions.modules.toolbar.splice(0, 0, [{ 'size': Size.whitelist }]);
        // quillOptions.modules.toolbar.push()
        quillOptions.modules.toolbar = [
            [{ "font": [] }, { 'size': Size.whitelist }],
            ["bold", "italic", "underline", "strike"],
            [{ "color": [] }, { "background": [] }],
            [{ "script": "sub" }, { "script": "super" }],
            // [{ "header": 1 }, { "header": 2 }, "blockquote", "code-block"],
            [{ "list": "ordered" }, { "list": "bullet" }, { "indent": "-1" }, { "indent": "+1" }],
            [{ "direction": "rtl" }, { "align": [] }],
            ["link", "image", "video", "formula"],
            ["clean"]
        ]

        this.quill = new Quill('#' + targetDivId, quillOptions);
        this.quill.on('text-change', () => {
            var delta = JSON.stringify(this.quill.getContents());
            var html = this.targetDiv.getElementsByClassName('ql-editor')[0].innerHTML;
            var data = {delta: delta, html: html};
            this.targetInput.value = JSON.stringify(data);
        });
    }
}


/* <div id="quillElementSelector" style="margin-bottom: 150px;">
</div>

<script src="quill-image-resize-module-master/image-resize.min.js"></script>
<script>
    var Size = Quill.import('attributors/style/size');
    Quill.register("modules/imageCompressor", imageCompressor);
    Quill.register("modules/resize", window.QuillResizeModule);
    // Quill.register('modules/imageDrop', ImageDrop)
    Quill.register('modules/imageResize', imageResize)
    Size.whitelist = ['14px', '16px', '24px'];
    Quill.register(Size, true);

    // var toolbarOptions = [
    //     [{ 'size': ['14px', '16px', '18px'] }],
    // ];

    var toolbarOptions = [
        ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
        ['blockquote', 'code-block'],

        [{ 'header': 1 }, { 'header': 2 }],               // custom button values
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
        [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
        [{ 'direction': 'rtl' }],                         // text direction

        [{ 'size': ['14px', '16px', '24px'] }],  // custom dropdown
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

        [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
        [{ 'font': [] }],
        [{ 'align': [] }],

        ['video'],
        ['link', 'image'],

        ['clean']                                         // remove formatting button
    ];

    var quill = new Quill("#quillElementSelector", {
        theme: 'snow',
        modules: {
            toolbar: toolbarOptions,
            imageResize: {
              displaySize: true // default false
            },
        }
    });

</script> */