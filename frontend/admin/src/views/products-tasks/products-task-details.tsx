import {Row, Col} from "antd";
import {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import productsTasksApi, {ProductsTaskResult} from "../../api/products-tasks";


export default function ProductsTaskDetails() {
    const [products, setProducts] = useState<ProductsTaskResult | null>(null);
    let params = useParams();


    useEffect(() => {
        async function fetchProducts(): Promise<ProductsTaskResult> {
            return await productsTasksApi.getProductTaskResult(params.taskId as string)
        }

        fetchProducts().then(result => {
            setProducts(result)
        });
    }, [params])

    const productItems = products?.results.map(
        (item, index) => (
            <Col xs={24} md={8} xl={6} key={`item-${index}`}>
                {item.url}
                <br />
                {item.imageUrl}
                <br />
                {item.discountPrice} - {item.price}
            </Col>
        )
    )

    return (
        <div>
            <h2>Discount Products</h2>
            <Row>
                {productItems}
            </Row>
        </div>
    )
}