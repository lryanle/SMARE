// chrome.commands.onCommand.addListener((command) => {
//   if (command === "new-listing") {
//     fetch('https://smare.lryanle.com/api/ext/stats', { cache: 'no-store', next: { revalidate: 0 } })
//     .then(response => response.json())
//     .then(data => {
//       window.location.href = data.data;
//       console.log(data.data)
//     })
//     .catch(error => {
//       console.error('Error:', error);
//     });
//   } else if (command === "flag-listing") {

//   } else if (command === "notflag-listing") {

//   } else if (command === "back-listing") {
//     window.history.back()
//   }
// })

chrome.runtime.onCommand.addListener((message, sender, sendResponse) => {
  if (message.action === 'new-listing') {
    fetch('https://smare.lryanle.com/api/ext/stats', { cache: 'no-store', next: { revalidate: 0 } })
        .then(response => response.json())
        .then(data => {
          const url = data.data
          chrome.tabs.create({ url })
          console.log(url)
        })
        .catch(error => {
          console.error('Error:', error);
        });
  }
});