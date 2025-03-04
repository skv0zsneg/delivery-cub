import { StarFill } from '@gravity-ui/icons';

import './Rate.css'

export default function Rate({ rateNumber }: {rateNumber: number}) {

    return (
        <div className="rate">
            <StarFill className="rate-icon" height={24} width={24} color="#FFBE5C"/>
            <span className="rate-number">{rateNumber}</span>
        </div>
    );
}