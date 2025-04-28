import Header from './Header';
import Footer from './Footer';

export default function Layout({ signOut, children }) {
  return (
    <>
      <Header signOut={signOut} />
      <div>{children}</div>
      <Footer />
    </>
  );
}
