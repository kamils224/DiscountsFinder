import {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import productsTasksApi, {ProductsTaskResult} from "../api/products-tasks";


export default function DiscountProducts() {
    const [products, setProducts] = useState<ProductsTaskResult | null>(null);
    let params = useParams();


    useEffect(() => {
        async function fetchProducts(): Promise<ProductsTaskResult> {
            return await productsTasksApi.getProductTaskResult(params.taskId as string)
        }
        fetchProducts().then(result => {
            setProducts(result)
        });
    }, [])

    return (
        <div>
            <h2>Discount Products</h2>
        </div>
    )
}