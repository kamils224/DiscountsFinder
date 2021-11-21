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

export class ProductItem {
    constructor(public url: string, public imageUrl: string, public discountPrice: string, public price: string) {
    }

    static fromJson(json: Record<string, any>) {
        return new ProductItem(json.url, json.image_url, json.discount_price, json.price);
    }
}

export class ProductsTaskResult extends ProductsTasks {
    constructor(public id: number,
                public timestamp: number,
                public status: string,
                public pageUrl: string,
                public count: number,
                public results: Array<ProductItem>) {
        super(id, timestamp, status, pageUrl, count);
    }

    static fromJson(json: Record<string, any>) {
        return new ProductsTaskResult(json._id, json.timestamp,
            json.status, json.page_url, json.count,
            json.results.map((item: Record<string, any>) => ProductItem.fromJson(item)))
    }
}

class ProductsTasksApi {

    baseUrl = "/api/discounts-finder";
    createTaskUrl = "/api/discounts-finder/process-single-url"
    deleteTaskUrl = "/api/discounts-finder/discounts-tasks"

    async getProductsTasks(): Promise<Array<ProductsTasks>> {
        const response = await axiosInstance.get(`${this.baseUrl}/discounts-tasks`);
        return response.data.map((item: Record<string, any>) => ProductsTasks.fromJson(item));
    }
    async getProductTaskResult(taskId: string): Promise<ProductsTaskResult> {
        const response = await axiosInstance.get(`${this.baseUrl}/discounts-tasks/${taskId}`);
        return ProductsTaskResult.fromJson(response.data);
    }
    async addTask(url: string): Promise<ProductsTasks> {
        const response = await axiosInstance.post(this.createTaskUrl, { url: url })
        return ProductsTasks.fromJson(response.data);
    }
    async deleteTask(objectId: string): Promise<boolean> {
        const response = await axiosInstance.delete(`${this.deleteTaskUrl}/${objectId}`)
        return response.status === 204;
    }
}

export default new ProductsTasksApi();