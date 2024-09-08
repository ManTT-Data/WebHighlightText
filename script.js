// Khởi tạo các biến toàn cục
let pdfDoc = null;
let pageNum = 1;
let pageRendering = false;
let pageNumPending = null;
const scale = 1.5;
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');

// Khởi tạo worker của PDF.js
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.9.359/pdf.worker.min.js';

// Hàm render trang PDF
function renderPages() {
    const pdfViewer = document.getElementById('pdfViewer');
    pdfViewer.innerHTML = ''; // Xóa nội dung cũ

    for (let num = 1; num <= pdfDoc.numPages; num++) {
        pdfDoc.getPage(num).then((page) => {
            const scale = 1.5;
            const viewport = page.getViewport({ scale: scale });
            
            // Tạo container cho mỗi trang
            const pageContainer = document.createElement('div');
            pageContainer.className = 'pdf-page';
            pdfViewer.appendChild(pageContainer);

            // Tạo và render canvas
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;
            pageContainer.appendChild(canvas);

            const renderContext = {
                canvasContext: ctx,
                viewport: viewport
            };

            page.render(renderContext);

            // Tạo và render text layer
            const textLayerDiv = document.createElement('div');
            textLayerDiv.className = 'textLayer';
            pageContainer.appendChild(textLayerDiv);

            // Thêm event listener cho việc select text
            textLayerDiv.addEventListener('mouseup', handleTextSelection);

            page.getTextContent().then(function(textContent) {
                pdfjsLib.renderTextLayer({
                    textContent: textContent,
                    container: textLayerDiv,
                    viewport: viewport,
                    textDivs: []
                });
            });

            // Thêm data-page-number attribute cho mỗi trang
            pageContainer.setAttribute('data-page-number', num);
        });
    }

    // Thêm event listener cho scroll sau khi render tất cả các trang
    pdfViewer.addEventListener('scroll', updateCurrentPage);
}

// Hàm cập nhật số trang hiện tại
function updateCurrentPage() {
    const pdfViewer = document.getElementById('pdfViewer');
    const pages = pdfViewer.getElementsByClassName('pdf-page');
    const scrollTop = pdfViewer.scrollTop;
    const viewerHeight = pdfViewer.clientHeight;

    for (let i = 0; i < pages.length; i++) {
        const page = pages[i];
        const pageTop = page.offsetTop - pdfViewer.offsetTop;
        const pageBottom = pageTop + page.offsetHeight;

        if (pageTop <= scrollTop && pageBottom > scrollTop) {
            const currentPage = page.getAttribute('data-page-number');
            document.getElementById('page_num').textContent = currentPage;
            break;
        }
    }
}

// Hàm xử lý việc select text
function handleTextSelection() {
    const selection = window.getSelection();
    const selectedText = selection.toString().trim();
    if (selectedText) {
        addHighlight(selectedText);
    }
}

// Hàm thêm highlight vào box
function addHighlight(text) {
    const highlightedText = document.getElementById('highlightedText');
    const highlightP = document.createElement('p');
    highlightP.textContent = text;
    highlightedText.appendChild(highlightP);
}

// Thêm event listener cho nút Clean
document.getElementById('cleanHighlights').addEventListener('click', function() {
    document.getElementById('highlightedText').innerHTML = '';
});

// Hàm tải và hiển thị PDF
function loadPDF(file) {
    const fileReader = new FileReader();

    fileReader.onload = function() {
        const typedarray = new Uint8Array(this.result);

        pdfjsLib.getDocument(typedarray).promise.then((pdf) => {
            pdfDoc = pdf;
            document.getElementById('page_count').textContent = pdf.numPages;
            renderPages();
            // Cập nhật số trang ban đầu
            document.getElementById('page_num').textContent = '1';
        });
    };

    fileReader.readAsArrayBuffer(file);
}

// Xử lý sự kiện khi người dùng tải lên file PDF
document.getElementById('pdfUpload').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file.type !== 'application/pdf') {
        alert('Vui lòng chọn file PDF');
        return;
    }
    loadPDF(file);
});

// Thêm canvas vào container
// document.getElementById('pdfViewer').appendChild(canvas);
