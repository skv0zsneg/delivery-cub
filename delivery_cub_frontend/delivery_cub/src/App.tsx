import Header from './components/header/Header';
import RestaurantCard from './components/restaurant_card/RestaurantCard';
import BreadCrumbs from './components/bread_crumbs/BreadCrumbs';


export default function App() {

  return (
    <>
      <Header />
      <br />
      <RestaurantCard
        restaurantName='Бургерная №1'
        restaurantRate={4.9}
        restaurantTitle='Вкусные и сочные бургеры' />
      <br />
      <BreadCrumbs
        currentPageName='Пользователи '
        pagesBehind={[
          { pageName: "Рестораны", pageUrl: "/" },
          { pageName: "Отзывы", pageUrl: "/dashboard" },
        ]}
      />
    </>
  )
}
