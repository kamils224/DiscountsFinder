import axiosInstance from "../axios-config/axios.instance";

export class ProductsTasks {
    constructor(public id: number,
                public timestamp: number,
                public status: string,
                public pageUrl: string,
                public count: number) {
    }

    static fromJson(json: Record<string, any>) {
        return new ProductsTasks(json._id, json.timestamp,
            json.status, json.page_url, json.count);
    }
}

export class DiscountProduct {
    constructor(public url: string, public imageUrl: string, public discountPrice: string, public price: string) {
    }

    static fromJson(json: Record<string, any>) {
        return new DiscountProduct(json.url, json.image_url, json.discount_price, json.price);
    }
}

export class ProductsTaskResult extends ProductsTasks {
    constructor(public id: number,
                public timestamp: number,
                public status: string,
                public pageUrl: string,
                public count: number,
                public results: Array<DiscountProduct>) {
        super(id, timestamp, status, pageUrl, count);
    }

    static fromJson(json: Record<string, any>) {
        return new ProductsTaskResult(json._id, json.timestamp,
            json.status, json.page_url, json.count,
            json.results.map((item: Record<string, any>) => DiscountProduct.fromJson(item)))
    }
}

class ProductsTasksApi {

    baseUrl = "/api/discounts-finder/discounts-tasks";

    async getProductsTasks(): Promise<Array<ProductsTasks>> {
        const response = await axiosInstance.get(this.baseUrl);
        return response.data.map((item: Record<string, any>) => ProductsTasks.fromJson(item));
    }
    async getProductTaskResult(taskId: string): Promise<ProductsTaskResult> {
        const response = await axiosInstance.get(`${this.baseUrl}/${taskId}`);
        return ProductsTaskResult.fromJson(response.data);
    }
}

export default new ProductsTasksApi();