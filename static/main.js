const loadContainer = document.getElementById("loadContainer");
const formOverlay = document.querySelector(".form-overlay")
const uploadSection = document.getElementById("uploadSection");
const file = document.getElementById("file")
const uploadForm = document.getElementById("uploadForm")
const parser = new DOMParser();
document.getElementById("uploadForm").addEventListener("submit", function(e) {
    e.preventDefault();
    changeElementStates(true);
    const formData = new FormData(this);
    fetch("/uploadFile", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        changeElementStates(false);
        showClusters(data);
    })
});

function changeElementStates(start)
{
    uploadSection.style.display = !start ? 'none' : 'flex';
    loadContainer.style.display = start ? 'flex' : 'none';
    var children = uploadForm.children;
    for(let i =0;i < children.length;i++)
    {
        children[i].disabled = !children[i].disabled;
    }
    formOverlay.style.display = start ? 'block' : 'none';
}

function showClusters(data)
{
clustersSection = document.getElementById("clusters");
let list = '<ul>';
for(let i = 0;i < Object.keys(data).length;i++)
{
    let clusterHeader = `<li><h3>Cluster ${i+1}:</h3></li>`;
    let clusterContent = '<li style="list-style-type:none;"><ul>';
    for(let j = 0; j < data[i].length;j++)
    {
        clusterContent += `<li>${data[i][j]}</li>`;
    }
    clusterContent += '</ul></li>';
    clusterHeader += clusterContent
    list+=clusterHeader;
}
list += '</ul>'
clustersSection.appendChild(parser.parseFromString(list,"text/html").getElementsByTagName("ul")[0]);
}