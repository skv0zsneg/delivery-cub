import { Card } from '@gravity-ui/uikit';

import Rate from '../rate/Rate';

import burgerPhoto from '../../assets/burger-photo.jpg'
import './RestaurantCard.css'

interface RestaurantCardProps {
    restaurantName: string;
    restaurantTitle: string;
    restaurantRate: number;
}

export default function RestaurantCard({restaurantName, restaurantTitle, restaurantRate}: RestaurantCardProps) {
    return (
        <Card className='restaurant-card' view="filled" size="l">
            <div className='restaurant-card-info'>
                <div className="restaurant-card-info-top">
                    <span className='restaurant-card-info-title'>{restaurantName}</span>
                    <Rate rateNumber={restaurantRate} />
                </div>
                <span className='restaurant-card-info-subtitle'>{restaurantTitle}</span>
            </div>
            <img className='restaurant-card-image' src={burgerPhoto} />
        </Card>
    );
}