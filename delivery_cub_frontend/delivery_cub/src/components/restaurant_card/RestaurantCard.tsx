import { Card } from '@gravity-ui/uikit';

import burgerPhoto from '../../assets/burger-photo.jpg'
import './RestaurantCard.css'

export default function RestaurantCard() {
    return (
        <Card className='restaurant-card' view="filled" size="l">
            <div className='restaurant-card-info'>
                <div className="restaurant-card-info-top">
                    <span className='restaurant-card-info-title'>Ресторан 1</span>
                    <span>* 4.5</span>  {/* TODO: оценка ресторан */}
                </div>
                <span className='restaurant-card-info-subtitle'>Короткое и лаконичное описание ресторана</span>
            </div>
            <img className='restaurant-card-image' src={burgerPhoto} />
        </Card>
    );
}