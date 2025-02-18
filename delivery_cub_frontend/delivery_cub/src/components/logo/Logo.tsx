import LogoSvg from '../../assets/logo.svg';
import './Logo.css';

export type LogoSize = "S" | "XL";

const sizeConfig: Record<LogoSize, { height: number; width: number }> = {
    S: { height: 50, width: 50 }, // Маленький размер
    XL: { height: 123, width: 123 }, // Большой размер
};

export default function Logo({ logoSize }: { logoSize: LogoSize }) {
    const { height, width } = sizeConfig[logoSize];

    return (
        <div className='logo'>
            <img
                src={LogoSvg}
                alt='delivery-cub-logo'
                height={height}
                width={width}
            />
            <span className='logo-name' >Delivery Cub</span>
        </div>
    )
}
