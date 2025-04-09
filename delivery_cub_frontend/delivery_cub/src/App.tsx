import { RestaurantApi } from './components/api/openapi_generated';
import axiosInstance from './components/api/axiosInstance';
import { login } from './components/api/auth';

import Header from './components/header/Header';
import RestaurantCard from './components/restaurant_card/RestaurantCard';
import BreadCrumbs from './components/bread_crumbs/BreadCrumbs';
import { useEffect, useState } from 'react';


export default function App() {
  const restaurantApi = new RestaurantApi(undefined, undefined, axiosInstance);
  const [restaurants, setRestaurants] = useState<any>([]);

  useEffect(() => {
    const fetchUsers = async () => {
      const response = await restaurantApi.restaurantList();
      setRestaurants(response.data);
      console.log(restaurants);
    };
    
    fetchUsers();
  }, []);
  
  // TODO: Нужно сделать форму авторизации
  // useEffect(() => {
  //   const fetchUsers = async () => {
  //     const response = await login("admin", "admin", axiosInstance);
  //     console.log(response);
  //   };

  //   fetchUsers();
  // }, []);

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
