import {Row, Col, Image, Card} from "antd";
import {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import productsTasksApi, {ProductsTaskResult} from "../../api/products-tasks";
import {calculateDiscount} from "../../utils/price-utils";


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
                <Card>
                    <a href={item.url} >
                        <Image preview={false} src={item.imageUrl} />
                    </a>
                    <br/>
                        {item.discountPrice} - <span style={{textDecoration: "line-through"}}>{item.price}</span>
                    <br/>
                    <h3 style={{color: "red"}}>
                        { Math.round(calculateDiscount(parseFloat(item.price), parseFloat(item.discountPrice))) }%
                    </h3>
                </Card>
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
