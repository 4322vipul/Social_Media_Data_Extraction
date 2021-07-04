import pandas as pd
from collections import defaultdict
import instaloader
from decorators import profile_function


class InfoExtraction:

    def __init__(self, login_info):
        self.client = instaloader.Instaloader()
        self.client.login(login_info['Username'], login_info['Password'])
        self.client.interactive_login(login_info['Username'])
        self.client.load_session_from_file(login_info['Username'])

    def execute_pipeline(self):
        full_information = list()
        profile_names = self.get_data()
        for name in profile_names:
            info_dict = self.extract_information_instagram(name=name)
            full_information.append(info_dict)
            print('Process done for', str(info_dict['Username']))
        result_dataframe = pd.DataFrame(full_information)
        return result_dataframe

    @profile_function
    def extract_information_instagram(self, name):
        info_dict = dict()
        profile = instaloader.Profile.from_username(self.client.context, name)
        info_dict['Username'] = profile.username
        info_dict['Name'] = profile.full_name
        info_dict['Profile_Picture_Link'] = profile.profile_pic_url
        info_dict['Bio'] = profile.biography
        info_dict['Followers'] = profile.followers
        info_dict['Total_Post'] = len([post for post in profile.get_posts()])

        # Extracting each persons post info
        info_dict['Post_Information'] = self.get_post_details(profile=profile)
        info_dict['Is_Business_Account'] = profile.is_business_account
        info_dict['Is_Verified'] = profile.is_verified
        return info_dict

    @staticmethod
    def get_post_details(profile):
        post_details = defaultdict(list)
        for index, post in enumerate(profile.get_posts()):
            post_details['Likes'].append(post.likes)
            post_details['Caption'].append(post.caption)
            post_details['Comments'].append(post.comments)
            post_details['Caption_Hashtags'].append(post.caption_hashtags)
            post_details['Post_Link'].append(post.url)
            if index > 4:
                break
        return post_details

    @staticmethod
    def get_data():
        influencers_df = pd.read_csv('D:\\Social_Media_Data_Extraction\\influencers_names.txt', delimiter=',')
        influencers_df = influencers_df.head(3)
        infulencers_list = influencers_df['Names'].tolist()
        return infulencers_list


if __name__ == "__main__":
    config = {"Username": "aim__headshot",
              "Password": ""}
    res_dataframe = InfoExtraction(config).execute_pipeline()
    print(res_dataframe.shape)
    res_dataframe.to_csv('D:\\Social_Media_Data_Extraction\\extracted_information.csv')
