export function calculateDiscount(price: number, discountPrice: number): number {
    return (1 - discountPrice/price) * 100;
}
