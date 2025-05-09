//STEP 1

let goToBottom = setInterval(() => window.scrollBy(0, 400), 1000);

//STEP 2:

    clearInterval(goToBottom);
    let arrayVideos = [];
    console.log('\n'.repeat(50));
    const containers = document.querySelectorAll('[class*="-DivItemContainerV2"]');  
    for (const container of containers) {
        const link = container.querySelector('[data-e2e="user-post-item"] a');
        const title = container.querySelector('[data-e2e="user-post-item-desc"] a');
        //If the link is https://www.tiktok.com/, set it as the current page URL
        if (link.href === 'https://www.tiktok.com/') link.href = window.location.href;
        arrayVideos.push(title.title + ';' + link.href);
        console.log(title.title + '\t' + link.href);
    }

//STEP 3:

    let data = arrayVideos.join('\n');
    let blob = new Blob([data], {type: 'text/csv'});
    let elem = window.document.createElement('a');
    elem.href = window.URL.createObjectURL(blob);
    elem.download = 'my_data.csv';
    document.body.appendChild(elem);
    elem.click();
    document.body.removeChild(elem);