import { GraduationCap, ShoppingCart } from '@gravity-ui/icons';
import { CreditCard } from '@gravity-ui/icons';
import { UserLabel } from '@gravity-ui/uikit';

import Logo from '../logo/Logo';
import './Header.css';

export default function Header() {
    return (
        <div className='header'>
            <Logo logoSize='S' />
            <div className="header-menu">
                <ShoppingCart height={40} width={40} color="#FFBE5C" />
                <CreditCard height={40} width={40} color="#FFBE5C" />
                <UserLabel
                    type="person"
                    avatar={{ icon: GraduationCap }}
                    text="UserName"
                    size="xl"
                />
            </div>
        </div>
    )
}