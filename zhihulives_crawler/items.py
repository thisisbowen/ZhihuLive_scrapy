# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field 

class LiveItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    liked = Field()
    sku_id = Field()
    live_type = Field()
    speaker_audio_message_count = Field()
    seats_taken = Field()
    seats_max = Field()
    in_promotion = Field()
    fee_original_price = Field()
    fee_amount = Field()
    fee_unit = Field()
    access_new_live = Field()
    source = Field()
    chapter_description = Field()
    type = Field()
    ends_in = Field()
    is_audition_open = Field()
    is_muted = Field()
    is_commercial = Field()
    is_live_owner = Field()
    is_admin = Field()
    artwork = Field()
    is_public = Field()
    review_count = Field()
    review_status = Field()
    review_score = Field()
    review_has_reviewed = Field()
    review_previous_status = Field()
    review_previous_score = Field()
    ends_at = Field()
    has_shutdown_permission = Field()
    is_anonymous = Field()
    audition_message_count = Field()
    buyable = Field()
    conv_id = Field()
    is_liked = Field()
    attachment_count = Field()
    vip_only = Field()
    recommendation_sku_id = Field()
    duration = Field()
    is_subscriber = Field()
    subject = Field()
    feedback_score = Field()
    description_html = Field()
    purchasable = Field()
    has_feedback = Field()
    id = Field()
    role = Field()
    income_amount = Field()
    income_unit = Field()
    has_authenticated = Field()
    reply_message_count = Field()
    status = Field()
    description = Field()
    speaker_message_count = Field()
    tags_0_score = Field()
    tags_0_name = Field()
    tags_0_short_name = Field()
    tags_0_available_num = Field()
    tags_0_created_at = Field()
    tags_0_great_num = Field()
    tags_0_id = Field()
    tags_0_live_num = Field()
    can_delete_message = Field()
    liked_num = Field()
    alert = Field()
    can_speak = Field()
    live_subscription_0_id = Field()
    live_subscription_0_title = Field()
    listened_progress = Field()
    outline = Field()
    has_audition = Field()
    audio_duration = Field()
    created_at = Field()
    anonymous_purchase = Field()
    starts_at = Field()
    is_refundable = Field()
    chapter_status = Field()
    speaker_id = Field()
    cospeakers = Field()
    audio_video_duration = Field()
    live_subscription = Field()
    live_subscription_1_id = Field()
    live_subscription_1_title = Field()
    recommendation = Field()
    crawl_time = Field()
    is_hot_monthly = Field()
    is_hot_weekly = Field()
    fee_end_time = Field()


class SpeakerItem(scrapy.Item):
    following_count = Field()
    shared_count = Field()
    included_text = Field()
    pins_count = Field()
    is_activity_blocked = Field()
    is_force_renamed = Field()
    lite_favorite_content_count = Field()
    headline = Field()
    participated_live_count = Field()
    is_bind_sina = Field()
    type = Field()
    following_topic_count = Field()
    sina_weibo_url = Field()
    answer_count = Field()
    articles_count = Field()
    name = Field()
    gender = Field()
    sina_weibo_name = Field()
    is_locked = Field()
    reactions_count = Field()
    hosted_live_count = Field()
    is_followed = Field()
    is_hanged = Field()
    user_type = Field()
    is_unicom_free = Field()
    marked_answers_text = Field()
    included_articles_count = Field()
    id = Field()
    favorite_count = Field()
    voteup_count = Field()
    live_count = Field()
    is_blocking = Field()
    following_columns_count = Field()
    is_baned = Field()
    is_enable_signalment = Field()
    is_enable_watermark = Field()
    following_favlists_count = Field()
    favorited_count = Field()
    open_ebook_feature = Field()
    follower_count = Field()
    description = Field()
    columns_count = Field()
    question_count = Field()
    url = Field()
    vip_info_is_vip = Field()
    included_answers_count = Field()
    following_question_count = Field()
    thanked_count = Field()
    independent_articles_count = Field()
    
    infinity_is_activated = Field()
    location_name = Field()
    education_name = Field()
    employment_name = Field()
    business_name = Field()
    badge_identity = Field()
    badge_type = Field()
    badge_topics = Field()
    
    
    crawl_time = Field()

class ReviewItem(scrapy.Item):
    crawl_time = Field()
    author_badge_avatar_url = Field()
    author_badge_id = Field()
    author_badge_name = Field()
    author_member_avatar_url = Field()
    author_member_gender = Field()
    author_member_headline = Field()
    author_member_id = Field()
    author_member_is_followed = Field()
    author_member_is_following = Field()
    author_member_member_role = Field()
    author_member_name = Field()
    author_member_type = Field()
    author_member_url = Field()
    author_member_url_token = Field()
    author_member_user_type = Field()
    author_role = Field()
    can_edit = Field()
    can_remove = Field()
    can_reply = Field()
    content = Field()
    created_at = Field()
    id = Field()
    is_gift_receiver = Field()
    own = Field()
    reply = Field()
    score = Field()
    updated_at = Field()

    live_id = Field()




    badge_identity = Field()
    badge_best_answerer = Field()
    badge_topics = Field()
    author_member_badge_icons_night = Field()
    author_member_badge_icons_normal = Field()
    '''
    updated_at = Field()
    created_at = Field()
    crawl_time = Field()
    live_id = Field()
    author_id = Field()
    author_url_token = Field()
    ticket = Field()
    role = Field()
    score = Field()
    content = Field()
    can_reply = Field()
    own
    can_remove
    id
    is_gift_receiver
    can_edit'''