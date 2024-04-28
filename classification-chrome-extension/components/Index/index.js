import styles from '../../styles/Pages.module.css';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import dynamic from 'next/dynamic';

export default function Index() {
  const [stats, setStats] = useState({
    sus: 0,
    notSus: 0,
    total: 0,
  });

  const router = useRouter();

  useEffect(() => {
    fetch('https://smare.lryanle.com/api/ext/stats', { cache: 'no-store', next: { revalidate: 0 } })
      .then(response => response.json())
      .then(data => {
        setStats(data.stats)
        console.log(data.stats)
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }, [])

  const handleLeft = () => {
    router.back()
  }

  const handleRight = () => {
    const ms = Date.now()
    fetch(`https://smare.lryanle.com/api/ext?dummy=${ms}`, { cache: "no-store", method: "GET"})
      .then(response => response.json())
      .then(data => {
        router.push(data.data)
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

  const handleUp = () => {
    fetch(`https://smare.lryanle.com/api/ext/label`, { cache: "no-store", method: "POST", body: JSON.stringify({label: "label-flagged"})})
      .then(response => response.json())
      .then(() => {
        fetch(`https://smare.lryanle.com/api/ext?dummy=${ms}`, { cache: "no-store", method: "GET"})
          .then(response => response.json())
          .then(data => {
            router.push(data.data)
          })
          .catch(error => {
            console.error('Error:', error);
          });
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

  const handleDown = () => {
    fetch(`https://smare.lryanle.com/api/ext/label`, { cache: "no-store", method: "POST", body: JSON.stringify({label: "label-notflagged"})})
    .then(response => response.json())
    .then(() => {
      fetch(`https://smare.lryanle.com/api/ext?dummy=${ms}`, { cache: "no-store", method: "GET"})
        .then(response => response.json())
        .then(data => {
          router.push(data.data)
        })
        .catch(error => {
          console.error('Error:', error);
        });
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }

  return (
    <div className={styles.container}>
      <main className={styles.main}>
        <div className={styles.stats}>
          {/* stats */}
          <div>
            {/* svg */}
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-flag"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" x2="4" y1="22" y2="15"/></svg>
            <span>
              {/* primary number */}
              {stats.totalFlagged.user}
              <span>
                {"/"}
                {stats.totalFlagged}
              </span>
            </span>
          </div>
          <hr className={styles.vertical}></hr>
          <div>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-flag-off"><path d="M8 2c3 0 5 2 8 2s4-1 4-1v11"/><path d="M4 22V4"/><path d="M4 15s1-1 4-1 5 2 8 2"/><line x1="2" x2="22" y1="2" y2="22"/></svg>
            <span>
              {/* primary number */}
                {stats.totalNotFlagged.user}
              <span>
                {"/"}
                {stats.totalNotFlagged}
              </span>
            </span>
          </div>
          <hr className={styles.vertical}></hr>
          <div>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-sigma"><path d="M18 7V4H6l6 8-6 8h12v-3"/></svg>
            <span>
              {/* primary number */}
                {stats.totalLabel.user}
              <span>
                {"/"}
                {stats.totalLabel}
              </span>
            </span>
          </div>
        </div>
        <hr className={styles.horizontal} />
        <div className={styles.wasd}>
          {/* control buttons */}
          <div>
            <button onClick={handleLeft}>
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="white" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-square-arrow-left"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="m12 8-4 4 4 4"/><path d="M16 12H8"/></svg>
              </div>
              <span>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-history"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/></svg>
                Back
              </span>
            </button>
          </div>
          <div>
            <button onClick={handleUp}>
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="white" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-square-arrow-up"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="m16 12-4-4-4 4"/><path d="M12 16V8"/></svg>
              </div>
              <span>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-flag"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" x2="4" y1="22" y2="15"/></svg>
                Sus
              </span>
            </button>
            <button onClick={handleDown}>
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="white" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-square-arrow-down"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="m8 12 4 4 4-4"/><path d="M12 8v8"/></svg>
              </div>
              <span>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-flag-off"><path d="M8 2c3 0 5 2 8 2s4-1 4-1v11"/><path d="M4 22V4"/><path d="M4 15s1-1 4-1 5 2 8 2"/><line x1="2" x2="22" y1="2" y2="22"/></svg>
                Not&nbsp;Sus
              </span>
            </button>
          </div>
          <div>
            <button onClick={handleRight}>
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="white" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-square-arrow-right"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="m12 16 4-4-4-4"/><path d="M8 12h8"/></svg>
              </div>
              <span>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-dice-6"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><path d="M16 8h.01"/><path d="M16 12h.01"/><path d="M16 16h.01"/><path d="M8 8h.01"/><path d="M8 12h.01"/><path d="M8 16h.01"/></svg>
                New
              </span>
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
