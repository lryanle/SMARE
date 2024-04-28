import styles from "./Footer.module.css";

export default function Footer() {
	return (
		<footer className={styles.footer}>
			<a
				href="https://github.com/lryanle/SMARE"
				target="_blank"
				rel="noopener noreferrer"
			>
				<span className={styles.logo}>
					<img src="icons/icon.svg" alt="Logo" width={16} height={16} className={styles.logo} />
				</span>
				SMARELA v1
			</a>
		</footer>
	);
}
